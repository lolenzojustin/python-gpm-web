import quopri
import re
from bs4 import BeautifulSoup

# Giả sử 'raw_email_content' là nội dung email bạn đã lấy về
raw_email_content = """Message-ID
<HP2v610000019bf1b7aab0ccaae6434b5c4360174@beauty.sephora.com>
Date
Sat, 24 Jan 2026 20:35:06 +0000
From
CustomerService@beauty.sephora.com
To
<lhn54o@lolenzo.com>
Subject
Verify your account
Authentication-Results
mx.zohomail.com; dkim=pass; spf=pass (zohomail.com: domain of beauty.sephora.com designates 142.54.245.176 as permitted sender) smtp.mailfrom=bounce@beauty.sephora.com; dmarc=pass(p=reject dis=none) header.from=beauty.sephora.com
Received
from [10.233.18.116] ([10.233.18.116:50334]) by pc1udsmtn2n19 (envelope-from <bounce@beauty.sephora.com>) (ecelerity 3.6.9.48312 r(Core:3.6.9.0)) with ECSTREAM id B5/DA-23978-AFC25796; Sat, 24 Jan 2026 20:35:06 +0000
Return-Path
<bounce@beauty.sephora.com>,<bounce@beauty.sephora.com>
Delivered-To: lhn54o@lolenzo.com
Received-SPF: pass (zohomail.com: domain of beauty.sephora.com designates 142.54.245.176 as permitted sender) client-ip=142.54.245.176; envelope-from=bounce@beauty.sephora.com; helo=mta176a.pmx1.epsl1.com;
Authentication-Results: mx.zohomail.com;
	dkim=pass;
	spf=pass (zohomail.com: domain of beauty.sephora.com designates 142.54.245.176 as permitted sender)  smtp.mailfrom=bounce@beauty.sephora.com;
	dmarc=pass(p=reject dis=none)  header.from=beauty.sephora.com
ARC-Seal: i=1; a=rsa-sha256; t=1769286906; cv=none; 
	d=zohomail.com; s=zohoarc; 
	b=KC4uA2Y20S8uE/bV2mi099Fvv+9ztsS4rKboilwFnBOBLba3ZGm7/cJUNjeonPzswylKjXd2lhyro7qurcLx7/g0EB72mX/WhlPv1x0w3SrILoWv3IjiJGPUWs7ARReI+p52QcIh95G1SOf+o8FA9UdtEC7zNQdapIOQTNRWpjo=
ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=zohomail.com; s=zohoarc; 
	t=1769286906; h=Content-Type:Date:Date:From:From:List-Unsubscribe:MIME-Version:Message-ID:Reply-To:Reply-To:Subject:Subject:To:To:Message-Id:Cc; 
	bh=adqsnIPq/9zCkApGEW1w47PznQdmomRbnmZYdhAelSo=; 
	b=R3Sm6PZqO+QJ00CXjm3uz2g4oJB9A7KGmsG3rXRjTM62iRG13taZb0xRuuRo+3zYFUgc+V76l+RpRhJafn1KQkLUXuSzhrzwGS5dqXrTTLPFDRZ2Y/1KG4hUYAagwdXEts0idzN/fyx5TQqapQZkFxRv0PmNO41eeX7JNuv+O+w=
ARC-Authentication-Results: i=1; mx.zohomail.com;
	dkim=pass;
	spf=pass (zohomail.com: domain of beauty.sephora.com designates 142.54.245.176 as permitted sender)  smtp.mailfrom=bounce@beauty.sephora.com;
	dmarc=pass header.from=<CustomerService@beauty.sephora.com> (p=reject dis=none)
Return-Path: <bounce@beauty.sephora.com>
Return-Path: <bounce@beauty.sephora.com>
Received: from mta176a.pmx1.epsl1.com (mta176a.pmx1.epsl1.com [142.54.245.176]) by mx.zohomail.com
	with SMTPS id 1769286906621278.48126607765573; Sat, 24 Jan 2026 12:35:06 -0800 (PST)
Received: from [10.233.18.116] ([10.233.18.116:50334])
	by pc1udsmtn2n19 (envelope-from <bounce@beauty.sephora.com>)
	(ecelerity 3.6.9.48312 r(Core:3.6.9.0)) with ECSTREAM
	id B5/DA-23978-AFC25796; Sat, 24 Jan 2026 20:35:06 +0000
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=beauty.sephora.com;
	s=ep1; t=1769286906;
	bh=adqsnIPq/9zCkApGEW1w47PznQdmomRbnmZYdhAelSo=;
	h=List-Unsubscribe:List-Unsubscribe-Post:MIME-Version:Subject:From:
	 To:Date:Content-Type;
	b=OvW1Cb1XLFzDlMV/OKwjQy61lgVoaI4wJiAtIMqxl7ThDlCLl6pq7LUBzV0ZNZFrK
	 lDzLze1rGJHhkT/rVjuGeEkU7VSOBZzavhjINm3ATdwDdPZVCXFUFLSFzLcyOzK/Ob
	 KsPXntPmxeOZIqK98RblCy09s6yELwTJ02x/SNaw=
List-Unsubscribe: <mailto:bounce-HP2v610000019bf1b7aab0ccaae6434b5c4360174@beauty.sephora.com?subject=list-unsubscribe>,<https://beauty.sephora.com/U2/v610000019bf1b7aab0ccaae6434b5c4360/03b9357276a347b6000001c1c0b84425>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
Message-ID: <HP2v610000019bf1b7aab0ccaae6434b5c4360174@beauty.sephora.com>
MIME-Version: 1.0
Feedback-ID: 03b93572-76a3-47b6-850b-95007ffa73b4:de0a3226-d396-4c2c-b3a8-3ede2f831505:email:epslh1
X-NSS: 03b93572-76a3-47b6-850b-95007ffa73b4
Reply-To: "support@beauty.sephora.com" <support@beauty.sephora.com>
Subject: Verify your account
From: Sephora  <CustomerService@beauty.sephora.com>
To: lhn54o@lolenzo.com
Date: Sat, 24 Jan 2026 20:35:06 +0000
Content-Type: multipart/alternative;
 boundary="-=Part.22f89c.94f089a0ada40d5f.19bf1b7b1b7.b60fb8479064f1f6=-"
X-ZohoMail-DKIM: pass (identity @beauty.sephora.com)

---=Part.22f89c.94f089a0ada40d5f.19bf1b7b1b7.b60fb8479064f1f6=-
Content-Transfer-Encoding: quoted-printable
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1=2E0 Transitional//EN"
"http://www=2Ew3=2Eorg/TR/xhtml1/DTD/xhtml1-transitional=2Edtd">
<html xmlns=3D"http://www=2Ew3=2Eorg/1999/xhtml" xmlns:v=3D"urn:schemas-mi=
crosoft-com:vml" xmlns:o=3D"urn:schemas-microsoft-com:office:office">
<head>
<meta http-equiv=3D"Content-Type" content=3D"text/html; charset=3Dutf-8" /=
>
<meta name=3D"viewport" content=3D"width=3Ddevice-width, initial-scale=3D1=
, maximum-scale=3D1" />
<meta http-equiv=3D"X-UA-Compatible" content=3D"IE=3DEdge" />
<meta name=3D"robots" content=3D"no index" />
<title>Sephora</title>
<style type=3D"text/css">=2EExternalClass * {line-height: 112%;}#outlook a=
 {padding: 0;}=2EExternalClass p, =2EExternalClass span, =2EExternalClass f=
ont, =2EExternalClass td {line-height: 112%;}a[href^=3Dtel], =2Enolinkcolor=
>a {color: inherit;text-decoration: none;}=2Esup, td {-webkit-text-size-adj=
ust: none;mso-line-height-rule: exactly;}=2EapplelinksGreyN a {color: #6d6e=
71 !important;text-decoration: none !important;}=2EapplelinksGreyN1, =2Eapp=
lelinksGreyN1 a {color: #6d6e71 !important;text-decoration: none !important=
;}table, td {border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspa=
ce: 0pt;padding: 0px;margin: 0px;mso-line-height-rule: exactly !important;}=
em {font-style: italic;}strong, b {font-weight: bold;}=2Esup {-webkit-text-=
size-adjust: none;}div, a, tr, table, body, span, img, strong, td {-webkit-=
text-size-adjust: none;-ms-text-size-adjust: none;-moz-text-size-adjust: no=
ne;text-size-adjust: none;-webkit-font-smoothing: antialiased;-moz-osx-font=
-smoothing: grayscale;}a[x-apple-data-detectors] {color: inherit !important=
;text-decoration: none !important;font-size: inherit !important;font-family=
: inherit !important;font-weight: inherit !important;line-height: inherit !=
important;}=2Ex-gmail-data-detectors, =2Ex-gmail-data-detectors *, =2EaBn {=
border-bottom: 0 !important;cursor: default !important;}=2Elink, =2Elink a =
{color: inherit !important;text-decoration: inherit !important;}#MessageVie=
wBody a {color: inherit;text-decoration: none;font-size: inherit;font-famil=
y: inherit;font-weight: inherit;line-height: inherit;}th {font-weight: norm=
al !important;}@media only screen and (max-width: 480px) {*[class=3Dhide_im=
g], =2Ehide_img {display: none!important;}*[class=3Dhide], =2Ehide {display=
: none !important;font-size: 0 !important;max-height: 0 !important;line-hei=
ght: 0 !important;padding: 0 !important;mso-hide: all !important;}*[class=
=3Dshow], =2Eshow {display: block !important;width: 100% !important;overflo=
w: visible !important;float: none !important;max-height: inherit !important=
;line-height: inherit !important;}*[class=3Dshow], =2Eshow {display: block!=
important;display: table!important;}*[class=3Dappear], =2Eappear {display: =
block !important;width: 100% !important;overflow: visible !important;float:=
 none !important;max-height: inherit !important;line-height: inherit !impor=
tant;}*[class=3Dappear], =2Eappear {display: block!important;display: table=
!important;}*[class=3Dtbl], =2Etbl {width: 100% !important;clear: both!impo=
rtant;float: inherit!important;height: auto !important;min-width: 100% !imp=
ortant;max-width: 100%!important;}*[class=3Dimg_full], =2Eimg_full {width: =
100% !important;height: auto !important;}*[class=3Dbreak], =2Ebreak {displa=
y: block!important;clear: both!important;}*[class=3Dappear], =2Eappear {dis=
play: block!important;display: table!important;}*[class=3Ddrop], =2Edrop {f=
loat: inherit!important;width: 100% !important;display: block !important;}*=
[class=3Dtext_ctr], =2Etext_ctr {text-align: center !important;}*[class=3Dt=
ext_lft], =2Etext_lft {text-align: left !important;}*[class=3Dtext_right], =
=2Etext_right {text-align: right !important;}*[class=3Dtbl_cntr], =2Etbl_cn=
tr {margin: 0 auto !important;}*[class=3DPad_hide], =2EPad_hide {padding: 0=
 !important;}*[class=3DPad_Thide], =2EPad_Thide {padding-top: 0 !important;=
}*[class=3DPad_Bhide], =2EPad_Bhide {padding-bottom: 0 !important;}*[class=
=3DPad_Lhide], =2EPad_Lhide {padding-left: 0 !important;}*[class=3DPad_Rhid=
e], =2EPad_Rhide {padding-right: 0 !important;}*[class=3DPad_hideLR], =2EPa=
d_hideLR {padding-left: 0 !important;padding-right: 0 !important;}*[class=
=3DPad_LR9], =2EPad_LR9 {padding-left: 9px !important;padding-right: 9px !i=
mportant;}*[class=3DnoneMobile], =2EnoneMobile {display: none;display: none=
 !important;}u~div =2Efull-wrap {min-width: 100vw;}div>u~div =2Efull-wrap {=
min-width: 100%;}*[class=3Dtopheaderc1], =2Etopheaderc1 {padding: 19px 0px =
25px 12px !important;}*[class=3DPad_LR15c1], =2EPad_LR15c1 {padding: 34px 9=
px 0px 10px !important;}*[class=3Dpadyellowboxc1], =2Epadyellowboxc1 {paddi=
ng: 19px 12px 17px 12px !important;}*[class=3DpadR0], =2EpadR0 {padding-rig=
ht: 0px !important;}*[class=3Dpadc1], =2Epadc1 {padding: 12px 25px 13px 25p=
x !important;}*[class=3Dpadc2], =2Epadc2 {padding: 19px 0px 18px 0px !impor=
tant;}*[class=3Dpadc3], =2Epadc3 {padding: 47px 0px 36px 0px !important;}*[=
class=3Dpadc4], =2Epadc4 {padding: 6px 50px 29px 50px !important;}*[class=
=3Dpadc5], =2Epadc5 {padding: 41px 0px 46px 0px !important;}*[class=3Dpadc6=
], =2Epadc6 {padding: 19px 0px 148px 0px !important;}*[class=3Dpadc7], =2Ep=
adc7 {padding: 50px 0px 49px 0px !important;}*[class=3Dpadc8], =2Epadc8 {pa=
dding: 15px 0px 159px 0px !important;}*[class=3Dpadc9], =2Epadc9 {padding: =
49px 0px 40px 0px !important;}*[class=3Dpadc10], =2Epadc10 {padding: 188px =
0px 0px 0px !important;}*[class=3Dpadc11], =2Epadc11 {padding: 48px 5px 30p=
x 5px !important;letter-spacing: 0px !important;font-size: 29px !important;=
line-height: 32px !important;}*[class=3Dpadc12], =2Epadc12 {padding: 36px 2=
5px 0px 25px !important;}*[class=3Dpadc13], =2Epadc13 {padding: 0px 30px 27=
px 30px !important;}*[class=3Dpad14], =2Epad14 {padding: 0px 25px 65px 25px=
 !important;}*[class=3DpadT6], =2EpadT6 {padding-top: 6px !important;}*[cla=
ss=3DpadT8], =2EpadT8 {padding-top: 8px !important;}*[class=3DpadB28], =2Ep=
adB28 {padding-bottom: 28px !important;}*[class=3DpadT10], =2EpadT10 {paddi=
ng-top: 10px !important;}*[class=3DpadB136], =2EpadB136 {padding-bottom: 13=
6px !important;}*[class=3DpadB148], =2EpadB148 {padding-bottom: 148px !impo=
rtant;}*[class=3Dimg240], =2Eimg240 {width: 240px !important;height: auto !=
important;}*[class=3DpadB13], =2EpadB13 {padding-bottom: 13px !important;}*=
[class=3DpadB9], =2EpadB9 {padding-bottom: 9px !important;}*[class=3Dbreak]=
, =2Ebreak {width: 100% !important;display: block !important;}*[class=3DlS0=
], =2ElS0 {letter-spacing: 1px !important;line-height: 35px !important;}*[c=
lass=3Dwdthauto], =2Ewdthauto {width: auto !important;margin: 0 auto !impor=
tant;}*[class=3DpadR20], =2EpadR20 {padding-right: 20px !important;}*[class=
=3Dwidth86], =2Ewidth86 {width: 86px !important;}*[class=3Dwidth35], =2Ewid=
th35 {width: 35px !important;}}</style><style type=3D"text/css">@media scre=
en yahoo {*[class=3Dinn], =2Einn {margin-top: 0% !important;padding: 0px 0p=
x !important;overflow: hidden !important;}*[class=3Dinn_share], =2Einn_shar=
e {margin-top: 0% !important;padding: 0px 0px !important;overflow: hidden !=
important;}*[class=3Dinner], =2Einner {margin-top: 0% !important;padding: 0=
px 0px !important;overflow: hidden !important;}}@media only screen and (max=
-width:480px) {=2EmobileBanner {font-size: 26px!important;line-height: 32px=
!important }=2EmobileCC {font-size: 48px!important;line-height: 54px!import=
ant }=2EmobileFooterText {font-size: 26px!important;line-height: 40px!impor=
tant }=2EmobileBelong {font-size: 60px!important;line-height: 80px!importan=
t }=2EmobileImgTierArrow {width: 10px!important }=2EmobileImgTier {height: =
60px!important }=2EmobileImgBday {width: 90px!important }=2EmobileImgCC {wi=
dth: 76px!important }=2EmobileImgCashHeader {width: 40px!important }=2Emobi=
leCashHeader {padding-left: 10px!important;line-height: 44px!important }=2E=
mobileImgCashFooter {width: 80px!important }=2EmobileCashBannerFooter {font=
-size: 40px!important;line-height: 48px!important }=2EmobileCashBannerFoote=
r2 {font-size: 28px!important;line-height: 36px!important }=2EmobileDisc {f=
ont-size: 24px!important;line-height: 30px!important }=2EmobileImgApp {widt=
h: 78px!important }=2EmobileImgFlash {width: 128px!important }=2EmobileImgF=
lashIcon {width: 52px!important }=2EmobileFooterTier {font-size: 42px!impor=
tant;line-height: 50px!important }=2EmobileFooterTierNonBI {font-size: 28px=
!important;line-height: 36px!important }=2EmobileFooterCTA {font-size: 28px=
!important;line-height: 36px!important }=2EmobileFooterImgTier {height: 70p=
x!important }=2EmobileFooterImgTierLogo {height: 80px!important }}</style><=
!--[if mso | ie]><style>body, table, td, span, a, strong, tr, font, sup {fo=
nt-family: Arial, Helvetica, sans-serif !important;}=2Esup {vertical-align:=
 1px !important;font-size: 100% !important;}body {background-color: #ffffff=
;}</style><![endif]--><!--[if ie]><style>=2Esup {vertical-align: 6px !impor=
tant;font-size: 80% !important;}</style><![endif]--><!--[if (gte mso 9)|(IE=
)]><style type=3D"text/css">table {border-collapse: collapse;border-spacing=
: 0;mso-line-height-rule: exactly;mso-margin-bottom-alt: 0;mso-margin-top-a=
lt: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;}</style><![endif]--><!--=
[if gte mso 9]><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch=
>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->
</head>
<body style=3D"margin: 0px; padding: 0px; background-color: #ffffff;  -web=
kit-text-size-adjust: none; -ms-text-size-adjust: none; text-size-adjust: n=
one; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscal=
e; padding:0; margin: 0; min-width: 100%">
<img src=3D'https://beauty=2Esephora=2Ecom/O/AQEAAZcF2gAndjYxMDAwMDAxOS1iZ=
jFiLTdhYWItMGNjYS1hZTY0MzRiNWM0MzYw2gAkMDNiOTM1NzItNzZhMy00N2I2LTAwMDAtNGM1=
YTQyOTYzYWEx2gAkMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwAw0OqdcZ01B=
13of959-ODwVHkLF1yXUd6rwPPPDySuQijcw' style=3D"display:none; max-height: 0p=
x; font-size: 0px; overflow: hidden; mso-hide: all"/> =20
   =20

<table width=3D"100%" border=3D"0" align=3D"center" cellpadding=3D"0" cell=
spacing=3D"0" bgcolor=3D"#ffffff" class=3D"full-wrap tbl_cntr">
  <tr>
    <td align=3D"center" bgcolor=3D"#ffffff" style=3D"vertical-align: top;=
 padding: 0px 0px 0px 0px">
      <!-- Gmail Wrapper -->
      <table width=3D"700" border=3D"0" cellspacing=3D"0" cellpadding=3D"0=
" style=3D"min-width:700px; width:700px; background-color: #ffffff;" bgcolo=
r=3D"#ffffff" class=3D"tbl tbl_cntr">
        <tr>
          <td align=3D"center" valign=3D"top">
            <table align=3D"center" bgcolor=3D"#FFFFFF" border=3D"0" cellp=
adding=3D"0" cellspacing=3D"0" width=3D"100%">
              <!--Preheader Text Start here-->
              <tr>
                <td align=3D"center" valign=3D"top">
                  <table width=3D"100%" border=3D"0" cellspacing=3D"0" cel=
lpadding=3D"0">
                    <tr>
                      <td align=3D"center" valign=3D"top"><div style=3D"di=
splay: none; max-height: 0px; overflow: hidden;">Complete your account setu=
p=2E <div style=3D"display: none; max-height: 0px; overflow: hidden;">&zwnj=
;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&n=
bsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp=
;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&n=
bsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp=
;&zwnj;&nbsp;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&n=
bsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp=
;&zwnj;&nbsp;&zwnj;&nbsp;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&n=
bsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp=
;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&z=
wnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj=
;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&z=
wnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj=
;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&nbsp;&zwnj;&nbsp;&z=
wnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj=
;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&nbsp;&z=
wnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj=
;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&n=
bsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp=
;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&z=
wnj;&nbsp;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp=
;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&z=
wnj;&nbsp;&zwnj;&nbsp;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp=
;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&z=
wnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp=
;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&z=
wnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
</div></div></td>
                    </tr>
                  </table>
                </td>
              </tr>
              <!--Preheader Text End here-->
              <tr>
                <td align=3D"center">

<!-- Missing CELL_CODE script -->=20
<!-- Yahoo Wrapper -->
<table width=3D"100%" border=3D"0" align=3D"center" cellpadding=3D"0" cell=
spacing=3D"0" bgcolor=3D"#ffffff" class=3D"full-wrap tbl_cntr">
<tr>
<td align=3D"center" bgcolor=3D"#ffffff" style=3D"vertical-align: top; pad=
ding: 0px 0px 0px 0px">
<!-- Gmail Wrapper -->
<table width=3D"700" border=3D"0" cellspacing=3D"0" cellpadding=3D"0" styl=
e=3D"min-width:700px; width:700px; background-color: #ffffff;" bgcolor=3D"#=
ffffff" class=3D"tbl tbl_cntr">
	<tr>
		<td align=3D"center" valign=3D"top">
		<table width=3D"100%" border=3D"0" cellspacing=3D"0" cellpadding=3D"0">
 =20
<!--Logo Section Start here-->
<tr>
	<td align=3D"center" valign=3D"top">
	<table width=3D"100%" border=3D"0" cellspacing=3D"0" cellpadding=3D"0">
    <tr>
   <td align=3D"center" valign=3D"top" style=3D"padding: 0px 0px 0px 0px; =
border-bottom: 1px solid #ffffff;"><a href=3D"https://beauty=2Esephora=2Eco=
m/T/v610000019bf1b7aab0ccaae6434b5c4360/03b9357276a347b60000021ef3a0bcc2/03=
b93572-76a3-47b6-850b-95007ffa73b4?__dU__=3Dv0G4RBKTXg2Gvf-dtDhFgyx2PTfuJRs=
WdK"  target=3D"_blank"><img src=3D"https://images=2Eharmony=2Eepsilon=2Eco=
m/ContentHandler/images/de0a3226-d396-4c2c-b3a8-3ede2f831505/images/2021_Na=
vs_Header_01_v4=2Epng" alt=3D"SEPHORA" width=3D"700" height=3D"auto" style=
=3D"display: block; border: 0;" /></a></td>
  </tr>    =20
</table>
	</td>
</tr>
<!--Logo Section End here-->
</table>

		</td>
	</tr>
</table>
<!-- /Gmail Wrapper -->
</td>
</tr>
</table>
<!-- Yahoo Wrapper --> </td>
              </tr>
              <tr>
                <td align=3D"left"><table border=3D"0" align=3D"center" ce=
llpadding=3D"0" cellspacing=3D"0">
<tr>
    <td style=3D"font-family: Arial, Helvetica, sans-serif; font-size: 16p=
x; padding: 30px 0px 16px 30px;" align=3D"left">
    You=E2=80=99re almost there! Finish setting up your online account to =
get all the benefits of Beauty Insider (like free shipping!)=2E Please veri=
fy below to confirm we have your correct email address=2E
    <br /><br />
    If you didn=E2=80=99t create this account, contact <a style=3D"color: =
blue; text-decoration: underline;" href=3D"https://beauty=2Esephora=2Ecom/T=
/v610000019bf1b7aab0ccaae6434b5c4360/03b9357276a347b60000021ef3a0bcc3/03b93=
572-76a3-47b6-850b-95007ffa73b4?__dU__=3Dv0G4RBKTXg2Gvf-dtDhFgyx2PTfuJRsWdK=
">Customer Service</a>=2E
    </td>
</tr>
<tr>
  <td align=3D"left" style=3D"padding-left: 30px"><a href=3D"https://beaut=
y=2Esephora=2Ecom/T/v610000019bf1b7aab0ccaae6434b5c4360/03b9357276a347b6000=
0021ef3a0bcc4/03b93572-76a3-47b6-850b-95007ffa73b4?__dU__=3Dv0G4RBKTXg2Gvf-=
dtDhFgyx2PTfuJRsWdK"><img style=3D"display:block;" border=3D"0" src=3D"http=
s://images=2Eharmony=2Eepsilon=2Ecom/ContentHandler/images/de0a3226-d396-4c=
2c-b3a8-3ede2f831505/images/US_Account_Verification_01=2Epng" width=3D"344"=
 height=3D"44" alt=3D"Verify Account" /></a></td>
</tr>
                   =20
<tr>
  <td style=3D"font-family: Arial, Helvetica, sans-serif; font-size: 16px;=
 padding: 16px 30px;" align=3D"left"><a style=3D"text-decoration: none; col=
or: #000;" href=3D"https://beauty=2Esephora=2Ecom/T/v610000019bf1b7aab0ccaa=
e6434b5c4360/03b9357276a347b60000021ef3a0bcc5/03b93572-76a3-47b6-850b-95007=
ffa73b4?__dU__=3Dv0G4RBKTXg2Gvf-dtDhFgyx2PTfuJRsWdK">Hurry, this link expir=
es in 24 hours=2E</a></td>
</tr>
</table></td>
              </tr>
              <tr>
                <td align=3D"center">

<!-- Missing CELL_CODE script -->=20
<!-- Yahoo Wrapper -->
<table width=3D"100%" border=3D"0" align=3D"center" cellpadding=3D"0" cell=
spacing=3D"0" bgcolor=3D"#ffffff" class=3D"full-wrap tbl_cntr">
<tr>
<td align=3D"center" bgcolor=3D"#ffffff" style=3D"vertical-align: top; pad=
ding: 0px 0px 0px 0px">
<!-- Gmail Wrapper -->
<table width=3D"700" border=3D"0" cellspacing=3D"0" cellpadding=3D"0" styl=
e=3D"min-width:700px; width:700px; background-color: #ffffff;" bgcolor=3D"#=
ffffff" class=3D"tbl tbl_cntr">
	<tr>
		<td align=3D"center" valign=3D"top">
		<table width=3D"100%" border=3D"0" cellspacing=3D"0" cellpadding=3D"0">
		=09
<tr>
<td align=3D"center" valign=3D"top" bgcolor=3D"#000000" style=3D"border-to=
p: 1px solid #ffffff; padding: 0px 20px;">
<table width=3D"100%" border=3D"0" cellspacing=3D"0" cellpadding=3D"0">
<tr>
<td align=3D"center" valign=3D"top" style=3D"border-top: 1px solid #ffffff=
;">
<table width=3D"100%" border=3D"0" cellspacing=3D"0" cellpadding=3D"0">
 <tr>
   <td align=3D"center" valign=3D"top" bgcolor=3D"#000000">
<table width=3D"100%" border=3D"0" cellspacing=3D"0" cellpadding=3D"0">
 <tr>
   <td align=3D"center" valign=3D"top" style=3D"color: #ffffff; padding: 5=
3px 0px 45px 0px;" class=3D"padc11"><a href=3D"https://beauty=2Esephora=2Ec=
om/T/v610000019bf1b7aab0ccaae6434b5c4360/03b9357276a347b60000021ef3a0bcc6/0=
3b93572-76a3-47b6-850b-95007ffa73b4?__dU__=3Dv0G4RBKTXg2Gvf-dtDhFgyx2PTfuJR=
sWdK"  target=3D"_blank" style=3D"color: #ffffff; text-decoration: none;"><=
span class=3D"link mobileBelong" style=3D"font-size: 40px; font-family: Geo=
rgia, 'serif';">We Belong to Something Beautiful</span></a></td>
  </tr>
  <tr>
	<td align=3D"center" valign=3D"top" style=3D"font-family: Arial, Helvetic=
a, sans-serif; color: #ffffff; font-size:13px; line-height:16px; mso-line-h=
eight-rule: exactly;" class=3D"lS0"><a href=3D"https://beauty=2Esephora=2Ec=
om/T/v610000019bf1b7aab0ccaae6434b5c4360/03b9357276a347b60000021ef3a0bcc7/0=
3b93572-76a3-47b6-850b-95007ffa73b4?__dU__=3Dv0G4RBKTXg2Gvf-dtDhFgyx2PTfuJR=
sWdK"  target=3D"_blank" style=3D"color: #ffffff; text-decoration: none;"><=
span class=3D"link mobileFooterText">Makeup</span></a><span class=3D"mobile=
FooterText">&nbsp;&nbsp;|&nbsp;&nbsp;</span><a href=3D"https://beauty=2Esep=
hora=2Ecom/T/v610000019bf1b7aab0ccaae6434b5c4360/03b9357276a347b60000021ef3=
a0bcc8/03b93572-76a3-47b6-850b-95007ffa73b4?__dU__=3Dv0G4RBKTXg2Gvf-dtDhFgy=
x2PTfuJRsWdK"  target=3D"_blank" style=3D"color: #ffffff; text-decoration: =
none;"><span class=3D"link mobileFooterText">Skincare</span></a><span class=
=3D"mobileFooterText">&nbsp;&nbsp;|&nbsp;&nbsp;</span><a href=3D"https://be=
auty=2Esephora=2Ecom/T/v610000019bf1b7aab0ccaae6434b5c4360/03b9357276a347b6=
0000021ef3a0bcc9/03b93572-76a3-47b6-850b-95007ffa73b4?__dU__=3Dv0G4RBKTXg2G=
vf-dtDhFgyx2PTfuJRsWdK"  target=3D"_blank" style=3D"color: #ffffff; text-de=
coration: none;"><span class=3D"link mobileFooterText">Hair</span></a><span=
 class=3D"mobileFooterText">&nbsp;&nbsp;|&nbsp;&nbsp;</span><a href=3D"http=
s://beauty=2Esephora=2Ecom/T/v610000019bf1b7aab0ccaae6434b5c4360/03b9357276=
a347b60000021ef3a0bcca/03b93572-76a3-47b6-850b-95007ffa73b4?__dU__=3Dv0G4RB=
KTXg2Gvf-dtDhFgyx2PTfuJRsWdK"  target=3D"_blank" style=3D"color: #ffffff; t=
ext-decoration: none;"><span class=3D"link mobileFooterText">Fragrance</spa=
n></a><span class=3D"hide">&nbsp;&nbsp;|&nbsp;&nbsp;</span><span class=3D"b=
reak"></span><a href=3D"https://beauty=2Esephora=2Ecom/T/v610000019bf1b7aab=
0ccaae6434b5c4360/03b9357276a347b60000021ef3a0bccb/03b93572-76a3-47b6-850b-=
95007ffa73b4?__dU__=3Dv0G4RBKTXg2Gvf-dtDhFgyx2PTfuJRsWdK"  target=3D"_blank=
" style=3D"color: #ffffff; text-decoration: none;"><span class=3D"link mobi=
leFooterText">Find a Store</span></a><span class=3D"mobileFooterText">&nbsp=
;&nbsp;|&nbsp;&nbsp;</span><a href=3D"https://beauty=2Esephora=2Ecom/T/v610=
000019bf1b7aab0ccaae6434b5c4360/03b9357276a347b60000021ef3a0bccc/03b93572-7=
6a3-47b6-850b-95007ffa73b4?__dU__=3Dv0G4RBKTXg2Gvf-dtDhFgyx2PTfuJRsWdK"  ta=
rget=3D"_blank" style=3D"color: #f53e4d; text-decoration: none;"><span styl=
e=3D"color: #f53e4d;" class=3D"link mobileFooterText">Get a Free Sample</sp=
an></a></td>
	</tr>
<tr>
<td align=3D"center" valign=3D"top">
<table width=3D"100%" border=3D"0" cellspacing=3D"0" cellpadding=3D"0">
 <tr>
   <td align=3D"center" valign=3D"top" style=3D"padding: 15px 0px 14px 0px=
;"><table width=3D"416" align=3D"center" border=3D"0" cellspacing=3D"0" cel=
lpadding=3D"0" class=3D"tbl">
 <tr>
	<th align=3D"left" valign=3D"top">
	 <table width=3D"100%" border=3D"0" cellspacing=3D"0" cellpadding=3D"0" c=
lass=3D"wdthauto">
  <tr>
	<td align=3D"center" valign=3D"top" style=3D"font-family: Arial, Helvetic=
a, sans-serif; color: #ffffff; font-size:13px; line-height:16px; mso-line-h=
eight-rule: exactly;" class=3D"lS0 mobileFooterText"><span class=3D"break">=
</span><a href=3D"https://beauty=2Esephora=2Ecom/T/v610000019bf1b7aab0ccaae=
6434b5c4360/03b9357276a347b60000021ef3a0bccd/03b93572-76a3-47b6-850b-95007f=
fa73b4?__dU__=3Dv0G4RBKTXg2Gvf-dtDhFgyx2PTfuJRsWdK"  target=3D"_blank" styl=
e=3D"color: #ffffff; text-decoration: none;"><span class=3D"link">Privacy P=
olicy</span></a><span class=3D"mobileFooterText">&nbsp;&nbsp;|&nbsp;&nbsp;<=
/span><a href=3D"https://beauty=2Esephora=2Ecom/T/v610000019bf1b7aab0ccaae6=
434b5c4360/03b9357276a347b60000021ef3a0bcce/03b93572-76a3-47b6-850b-95007ff=
a73b4?__dU__=3Dv0G4RBKTXg2Gvf-dtDhFgyx2PTfuJRsWdK"  target=3D"_blank" style=
=3D"color: #ffffff; text-decoration: none;"><span class=3D"link">Contact Us=
</span></a></td>
	</tr>
</table>
	 </th>
  </tr>
</table></td>
  </tr>
</table>=09
</td>=09
</tr>
<tr>
  <td align=3D"center" valign=3D"top" style=3D"font-family: Arial, Helveti=
ca, sans-serif; color: #ffffff; font-size:13px; line-height:16px; mso-line-=
height-rule: exactly; padding: 0px 10px 27px 10px; letter-spacing: 0=2E5px;=
" class=3D"padc13 mobileFooterText">&copy;2026 Sephora USA, Inc=2E, 350 Mis=
sion Street, Floor 7 San Francisco, <br class=3D"hide">CA 94105=2E All&nbsp=
;rights&nbsp;reserved=2E<br><a href=3D"https://beauty=2Esephora=2Ecom/H/2/v=
610000019bf1b7aab0ccaae6434b5c4360/03b93572-76a3-47b6-850b-95007ffa73b4/HTM=
L" style=3D"color: #000000; text-decoration: none;"><span class=3D"link">We=
b Version</span></a></td>
</tr>
<tr>
  <td align=3D"center" valign=3D"top" style=3D"font-family: Arial, Helveti=
ca, sans-serif; color: #acacac; font-size:12px; line-height:15px; mso-line-=
height-rule: exactly; padding: 0px 10px 20px 10px; letter-spacing: 0=2E5px;=
" class=3D"pad14 mobileDisc">Price and availability information is subject =
to change without notice, per our <a style=3D"color: #adadad;" href=3D"http=
s://beauty=2Esephora=2Ecom/T/v610000019bf1b7aab0ccaae6434b5c4360/03b9357276=
a347b60000021ef3a0bccf/03b93572-76a3-47b6-850b-95007ffa73b4?__dU__=3Dv0G4RB=
KTXg2Gvf-dtDhFgyx2PTfuJRsWdK"  target=3D"_blank">Terms of Use</a>=2E<br /><=
br />
Products and services may vary on sephora=2Ecom, at Sephora stores, in Sep=
hora at Kohl's stores, on kohl's=2Ecom/sephora, and on third-party marketpl=
aces=2E<br/><br/></td>
	</tr>
</table>=09
</td>
  </tr>
</table>=09
</td>		=09
</tr>	=09
<!--Footer Desclaimer section End here-->

</table>=09
</td>		=09
</tr>
	=09
</table>

		</td>
	</tr>
</table>
<!-- /Gmail Wrapper -->
</td>
</tr>
</table>
<!-- Yahoo Wrapper --></td>
              </tr>
            </table>
          </td>
        </tr>
       =20
      </table>
    </td>
  </tr>
</table>

<div style=3D"display:none; white-space:nowrap; font:15px courier; line-he=
ight:0;"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &n=
bsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; =
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; </div=
> =20
 =20
</body>
</html>
---=Part.22f89c.94f089a0ada40d5f.19bf1b7b1b7.b60fb8479064f1f6=---

"""

# 1. Giải mã Quoted-Printable
# Thêm .encode() đầu vào và errors='ignore' ở đầu ra
decoded_content = quopri.decodestring(raw_email_content.encode('utf-8')).decode('utf-8', errors='ignore')

# 2. Tìm link (Cách dùng BeautifulSoup - An toàn nhất)
soup = BeautifulSoup(decoded_content, 'html.parser')

# Tìm thẻ 'a' có chứa ảnh với alt='Verify Account' hoặc tìm theo link pattern
target_link = None
for a in soup.find_all('a', href=True):
    # Cách 1: Tìm theo ảnh bên trong
    img = a.find('img', alt="Verify Account")
    if img:
        target_link = a['href']
        break
    
    # Cách 2: Tìm theo text (nếu nút là text) hoặc pattern URL
    if "beauty.sephora.com/T/" in a['href']:
        target_link = a['href']
        # Lưu ý: Sephora thường có nhiều link track, link dài nhất thường là link verify chính
        
print(target_link)