# Нужно, т.к. библиотека Python обрабатывает docx, а не doc файлы. Требует Linux с установленным LibreOffice. Исполняется в корне git файла с данными. Дорогие поставщики данных, ну зачем было сохранять в .doc?
# Почему-то работает, только если есть запущенное окно LibreOffice
if command -v flatpak && flatpak list | grep -iq libreoffice; then
    libreoffice="flatpak run org.libreoffice.LibreOffice/x86_64/stable"
elif command -v LibreOffice; then
    libreoffice="LibreOffice"
elif command -v soffice; then
    libreoffice="soffice"
fi
cd data/Приложение\ №3
find -iname '*.doc' -exec $libreoffice --headless --convert-to docx {} {}x \;
cd ../Приложение\ №3\ \(2\)
find -iname '*.doc' -exec $libreoffice --headless --convert-to docx {} {}x \;
