"""Typed model for the tutorial catalog and per-tutorial metadata.

This module is the single definition of the metadata contract. Three consumers derive from it and
therefore cannot disagree with each other:

* ``generate_schema.py``   -- emits ``_shared/metadata/tutorial.schema.json`` from these models.
* ``validate_catalog.py``  -- parses every ``metadata.yml`` through them.
* ``export_landing_page.py`` -- builds the landing-page filter facets from the enums below.

Adding a filterable field means adding it here and nowhere else.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = REPO_ROOT / "tutorial_catalog.yml"
SCHEMA_PATH = REPO_ROOT / "_shared" / "metadata" / "tutorial.schema.json"

# Domain folders (others/, protein/, ...) sit directly at the repo root, so a tutorial path is
# "<domain>/<slug>" or "<domain>/<group>/<slug>". Everything that walks the tree goes through
# `Bucket.iter_relative_paths`; nothing else should join these path segments by hand.
TUTORIALS_ROOT = REPO_ROOT

# Root directories that are infrastructure, never tutorials. Used when discovering folders on disk.
NON_TUTORIAL_DIRS = {"_shared", "_build", "_gallery", "_pages", "_static", "scripts", "tests", ".git", ".github"}

SLUG_PATTERN = r"^[a-z][a-z0-9_]*$"


class Domain(str, Enum):
    """Top-level bucket. Fixed by the folder path, restated in metadata for the exporter."""

    OTHERS = "others"
    PROTEIN = "protein"
    CANCER = "cancer"
    CARDIAC = "cardiac"
    MATERIALS = "materials"


class Difficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Modality(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    GRAPH = "graph"
    TABULAR = "tabular"
    SEQUENCE = "sequence"
    OMICS = "omics"
    NEUROIMAGING = "neuroimaging"


class Fusion(str, Enum):
    """How multiple modalities are combined. ``none`` for single-modality tutorials."""

    NONE = "none"
    EARLY = "early"
    LATE = "late"
    INTERMEDIATE = "intermediate"
    TENSOR = "tensor"
    GRAPH = "graph"


class Hardware(str, Enum):
    CPU = "cpu"
    GPU_OPTIONAL = "gpu_optional"
    GPU_REQUIRED = "gpu_required"


class Dataset(BaseModel):
    """A dataset a tutorial can run against."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Human-readable dataset name, e.g. 'CIFAR-10'.")
    url: Optional[str] = Field(default=None, description="Where to obtain it.")
    size: Optional[str] = Field(default=None, description="Approximate download size, e.g. '170 MB'.")
    auto_download: bool = Field(default=False, description="True if the tutorial fetches it unattended.")


class TutorialMetadata(BaseModel):
    """Contract for every ``metadata.yml``. Mirrors ``_shared/templates/metadata.template.yml``."""

    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=1)

    title: str = Field(description="Gallery title. Sentence case, no trailing period.")
    slug: str = Field(pattern=SLUG_PATTERN, description="Folder name; must match the directory on disk.")
    summary: str = Field(min_length=20, max_length=400, description="One or two sentences for the gallery card.")

    domain: Domain
    task: str = Field(description="What the tutorial does, e.g. 'image classification'.")

    modality: List[Modality] = Field(min_length=1)
    method: List[str] = Field(min_length=1, description="Algorithms demonstrated, e.g. ['DANN', 'CDAN'].")
    fusion: Fusion = Fusion.NONE
    dataset: List[Dataset] = Field(default_factory=list)
    difficulty: Difficulty

    kale_api: List[str] = Field(default_factory=list, description="`kale` modules the tutorial exercises.")
    source_example: str = Field(description="Originating folder in pykale/examples, for provenance.")
    entry_point: str = Field(default="main.py")
    run_command: str = Field(description="Copy-pasteable command that runs the tutorial.")

    hardware: Hardware = Hardware.CPU
    estimated_runtime: str = Field(description="Wall-clock estimate on the stated hardware, e.g. '~5 min'.")

    colab: bool = Field(default=True, description="Offer a Colab badge.")
    binder: bool = Field(default=False, description="Offer a Binder badge.")
    draft: bool = Field(
        default=True,
        description="True while tutorial.py is still a stub; the example itself is runnable regardless.",
    )

    references: List[str] = Field(default_factory=list, description="Paper or repository URLs.")

    @field_validator("method", "kale_api", "references")
    @classmethod
    def _no_blanks(cls, value: List[str]) -> List[str]:
        if any(not item.strip() for item in value):
            raise ValueError("list entries must be non-empty")
        return value

    @property
    def is_runnable(self) -> bool:
        """Whether the narrative may be *executed* by the doc build and the nightly CI job.

        A tutorial runs only when its narrative is written (not a draft) and it does not require a
        GPU -- hosted CI has none. This is the single definition shared by the sphinx-gallery
        execution filter and ``scripts/list_runnable.py``, so the build and CI cannot disagree on
        what runs.

        Returns:
            bool: True if the tutorial is safe to execute on a CPU-only runner.
        """
        return not self.draft and self.hardware != Hardware.GPU_REQUIRED


class Group(BaseModel):
    """A sub-folder grouping related tutorials, e.g. ``others/image_classification``."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=SLUG_PATTERN)
    label: str
    tutorials: List[str] = Field(default_factory=list)


class BucketStatus(str, Enum):
    ACTIVE = "active"
    COMING_SOON = "coming_soon"


class Bucket(BaseModel):
    """A top-level domain folder."""

    model_config = ConfigDict(extra="forbid")

    id: Domain
    label: str
    color: str = Field(pattern=r"^#[0-9a-fA-F]{6}$", description="Accent colour used by the landing page.")
    summary: str
    # Presentation metadata, consumed by the homepage and domain pages. All optional so the catalog
    # stays valid without them; icon is an svg symbol id from _static/js/thumbnails (see custom.css).
    icon: str = Field(default="nodes", description="Domain symbol id used by thumbnails and cards.")
    examples: List[str] = Field(default_factory=list, description="One or two example topics for the card.")
    status: BucketStatus = Field(default=BucketStatus.ACTIVE)
    groups: List[Group] = Field(default_factory=list)
    tutorials: List[str] = Field(default_factory=list)

    def iter_relative_paths(self) -> List[str]:
        """List every tutorial in this bucket as a repo-relative path.

        Both directly-listed tutorials and those nested under a group are included.

        Returns:
            list[str]: Sorted repo-relative paths, e.g. ``["others/action_recognition",
            "others/image_classification/cifar_isonet"]``.
        """
        paths = [f"{self.id.value}/{slug}" for slug in self.tutorials]
        for group in self.groups:
            paths.extend(f"{self.id.value}/{group.id}/{slug}" for slug in group.tutorials)
        return sorted(paths)


class EcosystemEntry(BaseModel):
    """A related project shown in the homepage ecosystem section.

    ``url`` may be omitted for partners with no public link yet -- rendered as plain text, never a
    dead link.
    """

    model_config = ConfigDict(extra="forbid")

    name: str
    url: Optional[str] = None
    description: str
    planned: bool = Field(default=False, description="True for a future/announced project, badged as such.")


class LearningPath(BaseModel):
    """A curated ordered route through tutorials, by slug."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=SLUG_PATTERN)
    title: str
    summary: str
    tutorials: List[str] = Field(min_length=1, description="Tutorial slugs, in the order to take them.")


class Catalog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: int
    buckets: List[Bucket]
    ecosystem: List[EcosystemEntry] = Field(default_factory=list)
    learning_paths: List[LearningPath] = Field(default_factory=list)

    @classmethod
    def load(cls, path: Path = CATALOG_PATH) -> "Catalog":
        """Load and validate the catalog from a YAML file.

        Args:
            path: Path to ``tutorial_catalog.yml``. Defaults to the repo's catalog.

        Returns:
            Catalog: The validated catalog.

        Raises:
            pydantic.ValidationError: If the file does not match the schema.
        """
        return cls.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))

    def iter_relative_paths(self) -> List[str]:
        """List every tutorial across all buckets as a repo-relative path.

        Returns:
            list[str]: Repo-relative tutorial paths, in catalog (bucket) order.
        """
        paths: List[str] = []
        for bucket in self.buckets:
            paths.extend(bucket.iter_relative_paths())
        return paths

    def slug_to_path(self) -> dict[str, str]:
        """Map each tutorial slug to its repo-relative path.

        Returns:
            dict[str, str]: e.g. ``{"cifar_isonet": "others/image_classification/cifar_isonet"}``.
        """
        return {Path(path).name: path for path in self.iter_relative_paths()}
