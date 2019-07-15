reg='*25, XXXXXXX'
reg2='respCode=10072'
declare -A map=()
temp=''
temp2=""
while read line; do
  if [[ $line == $reg ]]; then
    temp=$($(echo ${line} | awk -F '[ |,]' '{print $5 }'))
    map["$temp"]="$temp"
  fi
  if [[ $line == $reg2 ]]; then
    temp2=$($(echo ${line} | awk -F '[ |,]' '{print $5 }'))
    for key in ${!map[@]}; do
      if [[ $key == $temp2 ]]; then
        echo $key
      fi
    done
  fi
done <common.log



