:: Нужно, т.к. библиотека Python обрабатывает docx, а не doc файлы. Требует Windows с установленным LibreOffice. Исполняется в корне git файла с данными. Дорогие поставщики данных, ну зачем было сохранять в .doc?
for %%f in ("data\Приложение №3\*.doc") do "C:\Program Files (x86)\LibreOffice\program\sooffice.exe" --headless --convert-to docx --outdir "data\Приложение №3\" "%%f"
for %%f in ("data\Приложение №3\*.DOC") do "C:\Program Files (x86)\LibreOffice\program\sooffice.exe" --headless --convert-to docx --outdir "data\Приложение №3\" "%%f"
for %%f in ("data\Приложение №3 (2)\*.doc") do "C:\Program Files (x86)\LibreOffice\program\sooffice.exe" --headless --convert-to docx --outdir "data\Приложение №3\" "%%f"
for %%f in ("data\Приложение №3 (2)\*.DOC") do "C:\Program Files (x86)\LibreOffice\program\sooffice.exe" --headless --convert-to docx --outdir "data\Приложение №3\" "%%f"
