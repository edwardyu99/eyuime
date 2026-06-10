cd ~
cp /mnt/c/Users/dad/OneDrive/eyuime/gcinrenee/renee.cin .

# 2. 轉換成正確的 Unix 格式 + UTF-8
dos2unix renee.cin
iconv -f utf-8 -t utf-8 -c renee.cin > renee_fixed.cin

# 3. 用修復後的檔案重新生成
mv renee_fixed.cin renee.cin

gcin2tab renee
cp renee.gtab /mnt/c/Users/dad/OneDrive/eyuime/gcinrenee/renee.gtab
ls -l
