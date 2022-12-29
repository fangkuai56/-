for x in ./*.wav
do 
  b=${x##*/}
  sox $b -r 22050 tmp_$b
  rm -rf $b
  mv tmp_$b $b
done
