pip freeze

pytest --cov=moban || goto :error

flake8 --max-line-length=88 --exclude=docs,.moban.d --ignore=W503,W504 || goto :error

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%
