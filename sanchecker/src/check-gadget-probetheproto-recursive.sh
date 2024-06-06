#out/Bytecode/chrome $URL --js-flags="--taint_log_file=/media/data1/zfk/Documents/sanchecker/crawl/testpath --no-crankshaft --no-turbo --no-ignition" --no-sandbox --disable-hang-monitor -enable-nacl&>log_file

#usage: sudo bash check-gadget-probetheproto-recursive.sh 0 1000 2 20

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/media/data1/zfk/Documents/capnproto-install/lib
export SAVE_PATH=/media/datak/inactive/sanchecker

start_line=$1
end_line=$2
if_flush=$3 # 1 for flush in path TAG="", 0 for flush in path TAG=<self_defined>, other for not flush
#sleep_time=$4
max_num_window=$4

rm -rf ~/.cache/chromium ~/.config/chromium
cd /tmp/
ls | grep -v systemd | xargs rm -rf
cd ${SAVE_PATH}/src
if ((if_flush == 1))
then
        # rm -rf ../crawl && mkdir ../crawl
        rm -rf logs && mkdir logs
        TAG=""
else
        #TAG="check_pp_pattern1_0to600kplus_" TAG="check_ppExploit_42_websites_url_src_to_pp_again_0to600kplus_"
        # TAG="check_NUMBER_ppExploit_2193_sites_" #"check_ppExploit_1212_vul_sites_" #"check_ppExploit_prev_vul_sites_" # 1212 means date 12/12/2021
	TAG="find_gadgets_probetheproto_"
        if ((if_flush == 0))
        then
                # rm -rf ../${TAG}crawl && mkdir ../${TAG}crawl
                rm -rf ${TAG}logs && mkdir ${TAG}logs
	else
		# mkdir -p ../${TAG}crawl
                mkdir -p ${TAG}logs
	fi
        
fi

cd /media/data1/zfk/Documents/sanchecker/src
#cd ~/Documents/chrome-linux
while IFS=, read -r idx url
do
    if (( idx > $start_line && idx <= $end_line ))
    then
            url="${url//[$'\t\r\n ']}" #remove newline from string
            NAME="${url/./_}"
            echo "${idx} ${url} ${TAG}logs/${NAME}_log_file sanchecker/${TAG}crawl/$NAME"
            ./out/Fast/chrome "${url}" \
                     --user-data-dir=/tmp/${NAME} --load-extension=/home/zfk/Documents/inject_pp_for_probetheproto_extension --new-window --disable-gpu --no-sandbox --disable-hang-monitor --enable-logging=stderr --v=1 &>${SAVE_PATH}/src/${TAG}logs/${NAME}_${idx}_log_file & #& pkill chrome > /dev/null &  #&>logs/${NAME}_log_file &
            # /media/data1/zfk/Documents/crawler-extension-pp,
            #--user-data-dir=/tmp/${NAME}\
            #         --user-data-dir=/home/zfk/Documents/usr_data_dir/${NAME}

            if (( (idx - ($start_line)) % $max_num_window == 0 ))
            then
                    echo "Waiting to clean $idx and prev $max_num_window windows ... "
                    # timeout 60 out/Bytecode/chrome $url --js-flags="--taint_log_file=/media/data1/zfk/Documents/sanchecker/${TAG}crawl/$NAME --no-crankshaft --no-turbo --no-ignition" \
                    # --new-window --no-sandbox --disable-hang-monitor -incognito -enable-nacl &>${TAG}logs/${NAME}_log_file && pkill chrome
                    sleep 35s
                    pkill chrome
                    sleep 1s
                    echo "$idx and prev $max_num_window windows cleaned! "
                    rm -rf ~/.cache/chromium ~/.config/chromium
        	    rm -rf ~/Downloads/*
                    sync; sh -c "echo 1 > /proc/sys/vm/drop_caches"    
	#else
                    
            fi
            #sleep ${sleep_time}s --user-data-dir=/tmp
    elif ((idx > $end_line))
    then
            echo "Come to the end $idx. Waiting to clean all windows ... "
            sleep 35s
            pkill chrome
            echo "All windows cleaned!"
            #echo "Finished and keep the windows to see if anything killed ... "
	    break
    fi
done < <(grep . ${SAVE_PATH}/src/tranco_LJ494.csv) #list_to_verify_new_vul.txt) #recrawl_705_sites_to_check_pp.txt) #crawl_all_url_vul_sites.txt) 
sleep 35s
pkill chrome
echo "All windows cleaned!"
#1212_recrawl_sites_to_check_pp.txt) #42_websites_url_src_to_pp_again_0to600kplus.txt)  #websites_total_to_pp_pattern1_0to600kplus.txt
#/media/data1/zfk/Documents/sanchecker/src/recursive_pp_pattern1_rankmorethan10k_logs/websites_to_pp.txt #tranco_94Q2.csv

#export FILE="./logs/${NAME}_log_file"
            #echo "logs/${NAME}_log_file"
            #CMD="out/Bytecode/chrome $url --js-flags=\"--taint_log_file=/media/data1/zfk/Documents/sanchecker/crawl/$NAME --no-crankshaft --no-turbo --no-ignition\" --no-sandbox --disable-hang-monitor -incognito -enable-nacl&>${NAME}_log_file"

#echo $CMD
            #bash -c $CMD
            #screen -S $idx -dm bash -c $CMD
