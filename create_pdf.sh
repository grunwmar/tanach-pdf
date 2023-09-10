cd tex
echo "Running xelatex..."
xelatex "$NAME"_"$LANG".tex #&> /dev/null
echo "Done."
mv "$NAME"_"$LANG".pdf ../pdfs/"$NAME"_"$LANG".pdf
cd ..

cp pdfs/"$NAME"_"$LANG".pdf "$EXPORT_DEST/$NAME"_"$LANG".pdf