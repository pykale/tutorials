@ECHO OFF
REM Windows equivalent of the Makefile targets.

pushd %~dp0

if "%PYTHON%" == "" (set PYTHON=python)
if "%BUILDDIR%" == "" (set BUILDDIR=_build)
set SPHINXOPTS=-W --keep-going

if "%1" == "" goto help
if "%1" == "help" goto help
if "%1" == "validate" goto validate
if "%1" == "schema" goto schema
if "%1" == "export" goto export
if "%1" == "pages" goto pages
if "%1" == "thumbnails" goto thumbnails
if "%1" == "homepage" goto homepage
if "%1" == "generate" goto generate
if "%1" == "lint" goto lint
if "%1" == "test" goto test
if "%1" == "html" goto html
if "%1" == "html-noplot" goto htmlnoplot
if "%1" == "clean" goto clean
echo Unknown target "%1". Run "make help".
goto end

:help
echo   validate     check catalog, metadata, schema and thumbnails agree
echo   schema       regenerate the metadata JSON schema
echo   export       regenerate the landing-page + source/_static tutorials.json
echo   pages        regenerate the per-domain pages
echo   thumbnails   regenerate the placeholder SVG thumbnails
echo   homepage     regenerate the homepage/list-page partials
echo   generate     run every generator
echo   lint         run pre-commit on all files
echo   test         run the script unit tests
echo   html         full build, executing runnable tutorials
echo   html-noplot  fast build with no tutorial execution
echo   clean        remove build artefacts
goto end

:validate
%PYTHON% scripts\generate_schema.py --check
if errorlevel 1 goto end
%PYTHON% scripts\validate_catalog.py
if errorlevel 1 goto end
%PYTHON% scripts\generate_thumbnails.py --check
goto end

:schema
%PYTHON% scripts\generate_schema.py
goto end

:export
%PYTHON% scripts\export_landing_page.py
goto end

:pages
%PYTHON% scripts\generate_bucket_pages.py
goto end

:thumbnails
%PYTHON% scripts\generate_thumbnails.py
goto end

:homepage
%PYTHON% scripts\generate_homepage.py
goto end

:generate
%PYTHON% scripts\generate_thumbnails.py
%PYTHON% scripts\generate_homepage.py
%PYTHON% scripts\generate_bucket_pages.py
%PYTHON% scripts\export_landing_page.py
goto end

:lint
pre-commit run --all-files
goto end

:test
%PYTHON% -m pytest
goto end

:html
call "%~f0" generate
%PYTHON% -m sphinx -b html %SPHINXOPTS% . %BUILDDIR%\html
goto end

:htmlnoplot
call "%~f0" generate
set TUTORIALS_NOPLOT=1
%PYTHON% -m sphinx -b html %SPHINXOPTS% . %BUILDDIR%\html
set TUTORIALS_NOPLOT=
goto end

:clean
if exist %BUILDDIR% rmdir /s /q %BUILDDIR%
if exist _gallery rmdir /s /q _gallery
if exist _pages rmdir /s /q _pages
if exist _generated rmdir /s /q _generated
if exist sg_execution_times.rst del /q sg_execution_times.rst
goto end

:end
popd
