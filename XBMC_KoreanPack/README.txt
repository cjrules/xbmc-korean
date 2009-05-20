뉴로스타님의 한글화 커스텀빌드팩입니다.

원문 : http://xbmc-korea.com/xe/develop/3116

1. 한글 기본 출력

GUISettings.cpp 에서 618 라인 한국어로 바꿉니다.

  AddString(2, "locale.language",248,"korean", SPIN_CONTROL_TEXT);



2. 스킨 한글화

포함 시킬 스킨의 각 해상도별 폴더안의 font.xml을 한글폰트로 만든 폰트셋이 포함되게 해야합니다.

PM III / PMIII HD 가 기본 스킨이지만, 엑스박스 버전이외에서 PH III스킨은 의미가 없으니 제거해도 됩니다.

대신 MediaStream 스킨의 완성도가 높으니 기본으로 포함시키면 좋을것 같습니다.

위 세 스킨의 font.xml을 넣어두었습니다.



3. 한글 폰트 추가

스킨의 font.xml안의 한글 폰트셋이 NanumGothicBold.ttf 와 SeoulNamsanM.ttf로 만들어진것이라

반드시 포함시켜야 하며, 나머지 폰트는 자막용으로 추가한것이니 편의에 따라 추가 삭제 하시면 되겠습니다.



4. 플러그인 / 스크래퍼

다음 3종 플러그인을 포함시키고, 다음, 네이버 스크래퍼에 업데이트 사항이 있으면 포함시킵니다.

무엇보다도 SVN Repo Installer를 포함시켜야 스킨이나 플러그인들을 XBMC내에서 받을수 있으니 

받드시 포함시킵니다.

맥 빌드에서는 itune 과 iphoto 플러그인을 기본으로 포함시키는게 좋을듯합니다.

http://code.google.com/p/xbmc-addons/downloads/list



이상의 커스텀 빌드를 하는데 필요한 모든 화일을 묶어 링크합니다.

http://xbmc-korean.googlecode.com/files/XBMC%20Korean%20Pack.rar