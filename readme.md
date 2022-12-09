# SIMPLE SOLAR SYSTEM 
🌌🌞🌏🪐🌌
---

## 🌞 설명
이름 : simple solar system
설명 : 



날짜에 따라 행성들의 대략적인 위치를 알 수 있고,
이를 통해 밤하늘에 행성의 위치를 대략적으로 파악할 수 있다.
이름에 'simple'이 있는 것처럼, 각 행성들의 궤도는 원으로 그렸고, 거리도 임의로 일정하게 그렸다.
많은 조건들이 생략되어서 실제 위치와는 오차가 있다.


![equinox](https://github.com/doremissong/simpleSolarSystem/blob/main/image/equinox.png)
제대로 동작하는지 확인을 편하게 하기 위해서 애플 천체 배경화면과 동일하게 **위쪽을 동지점**으로 두었다.

**sunpy**에서 얻을 수 있는 행성들의 정보는 해당 날짜에 지구에서 본 행성의 위치이기 때문에,
춘분점에서 해당 날짜의 지구 위치만큼 모든 행성들을 이동시켜주었다

main.py는 대부분 GUI와 관련된 내용이다.

simpleSolarSystem.py
; 행성들의 좌표, 날짜 계산 등을 한다.
 
🌏 __언어 & 라이브러리__
-- python (3.9)
-- PyQt5 (5.15.7) - GUI
-- matplotlib (3.5.2) - 그리기
-- sunpy (4.1.0)  - 위치 정보
-- astropy
-- webbrowser
-- datetime
-- sys


## 🌞 프로젝트 결과물

🌏 main window
![main window](https://github.com/doremissong/simpleSolarSystem/blob/main/image/mainWindow.gif) 
- simple solar system | info | exit 버튼
-

🌏 sss window
![sss window](https://github.com/doremissong/simpleSolarSystem/blob/main/image/sssWindow.gif)
- HOME 버튼, RESET 버튼, (+,-), dateEdit 위젯
- 

🌏 info window
![info window](https://github.com/doremissong/simpleSolarSystem/blob/main/image/infoWindow.gif)
- 태양과 행성 버튼을 누르면 설명을 보여줍니다.

비교
사진 


🌏License
이 프로젝트는 MIT 라이선스.

🌏이미지는 직접 제작하였습니다.
 

## 🌞 참고

PyQt5에 matplotlib 그래프를 그리는 방법 참고
https://m.blog.naver.com/hjinha2/221839259540

matplotlib image marker 참고
https://www.tutorialspoint.com/how-to-use-a-custom-png-image-marker-in-a-plot-matplotlib

PyQt5 사용방법
https://wikidocs.net/37787

행성, 태양 정보
https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html
https://astro.kasi.re.kr/learning/pageView/5116

애플 천체 배경화면
태양계 모형이 제대로 동작하는지 확인하고, 방향을 잡을 때  애플의 천체 배경화면을 참고했다.


---
잡다

태양계 모형을 만들어보고 싶었다.