#out/Bytecode/chrome $URL --js-flags="--taint_log_file=/media/data1/zfk/Documents/sanchecker/crawl/testpath --no-crankshaft --no-turbo --no-ignition" --no-sandbox --disable-hang-monitor -enable-nacl&>log_file

#usage: sudo bash inactive-phase2-partial.sh 0 10000 2 5 0 2>&1 | tee -a ./inactive_notemplate_phase2_crawling.log

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/media/data1/zfk/Documents/capnproto-install/lib
# export SAVE_PATH=/home/zfk/Documents/sanchecker
export SAVE_PATH=/media/datak/inactive/sanchecker

start_line=$1
end_line=$2
if_flush=$3 # 1 for flush in path TAG="", 0 for flush in path TAG=<self_defined>, other for not flush
#sleep_time=$4
max_num_window=$4
if_clear_taint_log_files=$5 # 1 for not using taint log files

rm -rf ~/.cache/chromium ~/.config/chromium
cd /tmp/
ls | grep -v systemd | xargs rm -rf
# rm -rf /tmp/*_com* /tmp/*_net /tmp/*_org /tmp/*_io /tmp/*_edu* /tmp/*cn /tmp/*_uk /tmp/*_fr /tmp/*jp /tmp/*gov /tmp/google* /tmp/zo* /tmp/www* /tmp/*co /tmp/*ir
cd ${SAVE_PATH}/src
if ((if_flush == 1))
then
        rm -rf ../crawl && mkdir ../crawl
        rm -rf logs && mkdir logs
        TAG=""
else
        #TAG="check_pp_pattern1_0to600kplus_"
        TAG="inactive_notemplate_phase2_partial_"
	if ((if_flush == 0))
        then
                rm -rf ../${TAG}crawl && mkdir ../${TAG}crawl && chmod 777 ../${TAG}crawl
                rm -rf ${TAG}logs && mkdir ${TAG}logs && chmod 777 ${TAG}logs
	else
		mkdir -p ../${TAG}crawl && chmod 777 ../${TAG}crawl
                mkdir -p ${TAG}logs && chmod 777 ${TAG}logs
	fi
        
fi

cd /media/data1/zfk/Documents/sanchecker/src

while IFS=, read -r idx url
do
    if (( idx > $start_line && idx <= $end_line ))
    then
            url="${url//[$'\t\r\n ']}" #remove newline from string
            NAME="${url/./_}"
            rm -rf /tmp/${NAME}
            echo "${idx} ${url} ${TAG}logs, ${NAME}" #_log_file sanchecker/${TAG}crawl/$NAME"
            out/Inactive-release-phase2/chrome ${url} --js-flags="--taint_log_file=${SAVE_PATH}/${TAG}crawl/$NAME --no-crankshaft --no-turbo --no-ignition --undef_prop_dataset_file=/media/datak/inactive/analysis/phase1/output/undef_prop_dataset.json" \
                     --user-data-dir=/tmp/${NAME} --load-extension=/home/zfk/Documents/crawler-extension-pp --new-window --no-sandbox --disable-gpu --enable-logging=stderr --disable-hang-monitor &>${SAVE_PATH}/src/${TAG}logs/${NAME}_log_file & #& pkill chrome > /dev/null &  #&>logs/${NAME}_log_file &
            #--user-data-dir=/tmp/${NAME}

            if (( (idx - ($start_line)) % $max_num_window == 0 ))
            then
                    echo "Waiting to clean $idx and prev $max_num_window windows ... "
                    # timeout 60 out/Bytecode/chrome $url --js-flags="--taint_log_file=/media/data1/zfk/Documents/sanchecker/${TAG}crawl/$NAME --no-crankshaft --no-turbo --no-ignition" \
                    # --new-window --no-sandbox --disable-hang-monitor -incognito -enable-nacl &>${TAG}logs/${NAME}_log_file && pkill chrome
                    sleep 80s
                    pkill chrome
                    sleep 2s
                    pkill chrome
                    sleep 2s
                    echo "$idx and prev $max_num_window windows cleaned! "
                    # remove user-data in /tmp/ ; remove useless downloaded files; drop caches
                    cd /tmp/
                    ls | grep -v systemd | xargs rm -rf
		    # When not using taint log files in the crawl/
		    if (( if_clear_taint_log_files == 1))
		    then
		    	rm -rf ${SAVE_PATH}/${TAG}crawl/*
                    fi
		    rm -rf /home/zfk/Downloads/*
                    sync; sh -c "echo 1 > /proc/sys/vm/drop_caches"
                    cd /media/data1/zfk/Documents/sanchecker/src
		#     rm -rf /tmp/*_com /tmp/*_net /tmp/*_org /tmp/*_io /tmp/*_edu* /tmp/*_cn /tmp/*_uk
                
            #else
                    
            fi
            #sleep ${sleep_time}s --user-data-dir=/tmp
    elif ((idx > $end_line))
    then
            echo "Come to the end $idx. Waiting to clean all windows ... "
            sleep 80s
            pkill chrome
            echo "All windows cleaned!"
            #echo "Finished and keep the windows to see if anything killed ... "
	    break
    fi
# Note: the current tranco_3Z3L.csv gets rid of websites with domain '.pl'
# The bash cmd is: sudo sed -i.old '/.*\.pl/d' tranco_3Z3L.csv
done < <(grep . /media/datak/inactive/sanchecker/src/site_list_phase2_flow_not_found.csv) #/home/zfk/Documents/sanchecker/src/Inactive/sites_with_def_val_2.csv) #websites_total_to_pp_pattern1_600kto1m.txt) #42_websites_url_src_to_pp_again_0to600kplus.txt)  #websites_total_to_pp_pattern1_0to600kplus.txt #websites_to_pp_pattern1_0to200k.txt
#/media/data1/zfk/Documents/sanchecker/src/recursive_pp_pattern1_rankmorethan10k_logs/websites_to_pp.txt #tranco_94Q2.csv
sleep 80s
pkill chrome 
echo "All windows cleaned!"
# Previous unsuccessful cmd FYI
#export FILE="./logs/${NAME}_log_file"
            #echo "logs/${NAME}_log_file"
            #CMD="out/Bytecode/chrome $url --js-flags=\"--taint_log_file=/media/data1/zfk/Documents/sanchecker/crawl/$NAME --no-crankshaft --no-turbo --no-ignition\" --no-sandbox --disable-hang-monitor -incognito -enable-nacl&>${NAME}_log_file"

#echo $CMD
            #bash -c $CMD
            #screen -S $idx -dm bash -c $CMD
