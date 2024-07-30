find ./XMAIL -name '*.xm*l' -print | while read f; do
  echo "### loading $f ..."
  sh ./app/Script/load-xmail-REST.sh "$f"
  echo "### done."
done
