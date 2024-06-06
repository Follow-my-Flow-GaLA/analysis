CHROME_PATH="/home/zfk/Documents/chrome-linux/chrome"
EXTENSION_ID="your_extension_id"

# Base URL for the extension's page
EXTENSION_URL="chrome-extension://$EXTENSION_ID/your_extension_page.html"

# Arguments to pass to the extension
var_name="defaultValue"
payload="0px 0px 0px 0px #999"

# Construct the URL with query parameters
FULL_URL="$EXTENSION_URL?var_name=$ARG1&payload=$ARG2"

# Launch Chrome with the extension and the constructed URL
"$CHROME_PATH" --load-extension="$HOME/.config/google-chrome/Default/Extensions/$EXTENSION_ID" "$FULL_URL"

alias validate_phase3_db_runexe='sudo /home/zfk/Documents/chrome-linux/chrome https://viamichelin.com/?K1.K2=V --js-flags="--taint_log_file=/media/data1/zfk/Documents/sanchecker/testdir/viamichelin_com --phase3_enable --current_site=viamichelin.com --no-crankshaft --no-turbo" --user-data-dir=/tmp/test_chromium --load-extension=/home/zfk/Documents/validate_pp_extension/ --new-window --no-sandbox --disable-hang-monitor --disable-gpu --ignore-certificate-errors --allow-insecure-localhost --enable-logging=stderr --v=1 &> /home/zfk/temp/validate_phase3_db_viamichelin_com_log_file'

