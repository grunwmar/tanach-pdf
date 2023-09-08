cd tex
echo "Running xelatex..."
xelatex "$NAME".tex #&> /dev/null
echo "Done."
mv "$NAME".pdf ../pdfs/"$NAME".pdf
cd ..

cp pdfs/"$NAME".pdf "$EXPORT_DEST/$NAME".pdf