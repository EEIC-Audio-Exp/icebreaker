# 音声合成エンジンのpath
#jtalkbin = '/usr/local/open_jtalk-1.07/bin/open_jtalk '
#options = ' -m syn/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /usr/local/open_jtalk-1.07/dic'

# 音声合成のコマンドを生成 (open jtalk を 使う場合
def mk_jtalk_command(
    speak_str: str,
    jtalkbin: str = '/usr/bin/open_jtalk ',
    options: str = '-m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic',
):
    jtalk = 'echo "' + speak_str + '" | ' + jtalkbin + options + ';'
    play = 'play -q /tmp/dialogue/out.wav; rm /tmp/dialogue/out.wav;'
    return jtalk + play
