pyinstaller -D ./llc_win_wxPython.py -i ./resources/LLC_LOGO_OK_PLAIN_BANNER.ico --hide-console minimize-late --clean -n 伶伦转换器
pause
python ./clean_pycache.py