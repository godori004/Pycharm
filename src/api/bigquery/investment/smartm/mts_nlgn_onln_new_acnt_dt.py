# -*- coding: utf-8 -*-
# CREATER : 호이춘

import sys
import os
import time
from src.googleutil import bigquery
from datetime import datetime


def delete_mts_nlgn_onln_new_acnt_dt(c_stdr_dt) :
	try:
		client = bigquery.Client()
		# Perform a query.
		QUERY = ("DELETE FROM `hanwha-ga360.DT_STDO.MTS_NLGN_ONLN_NEW_ACNT_DT` WHERE DATE='"+c_stdr_dt+"'")
		print ("QUERY : %s " % QUERY)
		query_job = client.query(QUERY).to_dataframe()    # API request
		
	except Exception as ex:
		print("delete_mts_nlgn_onln_new_acnt_dt 에러 발생 !!!!!! %s " % ex)		
		endTime = time.time()
		etime=time.localtime(endTime)
		print ("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
		print ("수행시간 : %d 초" % (endTime-startTime))
		sys.exit(1)

def insert_mts_nlgn_onln_new_acnt_dt(stdr_dt,c_stdr_dt) :
	try:
		client = bigquery.Client()
		# Perform a query.
		QUERY = ( "INSERT INTO `hanwha-ga360.DT_STDO.MTS_NLGN_ONLN_NEW_ACNT_DT`               \n"    
              "SELECT A.DATE                                                              \n"
              "     , A.DTL_CD_NM AS STEP_NM                                              \n"
              "     , IFNULL(C.VCNT,0) AS VIEW_CNT                                        \n"
              "     , IFNULL(B.UCNT,0) AS USER_CNT                                        \n"
              "  FROM (SELECT PARSE_TIMESTAMP('%Y%m%d','"+stdr_dt+"') AS DATE, DTL_CD_NM  \n"
              "          FROM `hanwha-ga360.DT_STDO.DAL_CD_MST`                           \n"
              "         WHERE CTGR_CLSFCT_CD='NLGN_ONLN_NEW_ACNT'                         \n"
              "       ) A                                                                 \n"
              "  LEFT OUTER JOIN                                                          \n"
              "       (SELECT DATE AS DATE                                                \n"
              "            , CASE WHEN ScreenName IN ('비로그인_비대면개설_메인'           , '비대면개설_비로그인_메인'           ) THEN '01단계_비로그인_비대면개설_메인'    \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_계좌선택'       , '비대면개설_비로그인_계좌선택'       ) THEN '02단계_비로그인_비대면개설_계좌선택'   \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_휴대폰본인인증' , '비대면개설_비로그인_휴대폰본인인증' ) THEN '03단계_비로그인_비대면개설_휴대폰본인인증'  \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_약관동의'       , '비대면개설_비로그인_약관동의'       ) THEN '04단계_비로그인_비대면개설_약관동의'   \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_고객정보입력'   , '비대면개설_비로그인_고객정보입력'   ) THEN '05단계_비로그인_비대면개설_고객정보입력'  \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_계좌인증'       , '비대면개설_비로그인_계좌인증'       ) THEN '06단계_비로그인_비대면개설_계좌인증'   \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_인증번호입력'   , '비대면개설_비로그인_인증번호입력'   ) THEN '07단계_비로그인_비대면개설_인증번호입력'  \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_신분증촬영'     , '비대면개설_비로그인_신분증촬영'     ) THEN '08단계_비로그인_비대면개설_신분증촬영'   \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_신분증촬영_결과', '비대면개설_비로그인_신분증촬영_결과') THEN '09단계_비로그인_비대면개설_신분증촬영_결과' \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_신청완료'       , '비대면개설_비로그인_신청완료'       ) THEN '10단계_비로그인_비대면개설_신청완료'   \n"
              "              ELSE ScreenName END AS STEP                            \n"                                                                                                                                                                                                        
              "            , COUNT(DISTINCT SID) AS UCNT                            \n"                                                                         
              "         FROM `hanwha-ga360.DT_STDO.MTS_SCRN_VW_CNT_DT`              \n"                                                                         
              "        WHERE DATE='"+c_stdr_dt+"' AND                               \n"                                                                           
              "          SID IN (SELECT  SID                                        \n"                                                                         
              "                    FROM `hanwha-ga360.DT_STDO.MTS_SCRN_VW_CNT_DT`   \n"                                                                         
              "                   WHERE DATE='"+c_stdr_dt+"'                        \n"                                                                           
              "                   GROUP BY SID                                      \n"                                                                         
              "                  HAVING MAX(CASE WHEN ScreenName IN ('비로그인_비대면개설_메인', '비대면개설_비로그인_메인') THEN 1 ELSE 0 END) =1 \n" 
              "                 )                                                                                                     \n"                       
              "          AND screenName IN (  '비로그인_비대면개설_메인','비대면개설_비로그인_메인'                                                \n"                       
              "                             , '비로그인_비대면개설_계좌선택','비대면개설_비로그인_계좌선택'                                          \n"                       
              "                             , '비로그인_비대면개설_휴대폰본인인증','비대면개설_비로그인_휴대폰본인인증'                                 \n"                    
              "                             , '비로그인_비대면개설_약관동의','비대면개설_비로그인_약관동의'                                          \n"                       
              "                             , '비로그인_비대면개설_고객정보입력','비대면개설_비로그인_고객정보입력'                                    \n"                    
              "                             , '비로그인_비대면개설_계좌인증','비대면개설_비로그인_계좌인증'                                          \n"                       
              "                             , '비로그인_비대면개설_인증번호입력','비대면개설_비로그인_인증번호입력'                                    \n"                    
              "                             , '비로그인_비대면개설_신분증촬영','비대면개설_비로그인_신분증촬영'                                       \n"                       
              "                             , '비로그인_비대면개설_신분증촬영_결과','비대면개설_비로그인_신분증촬영_결과'                               \n"                    
              "                             , '비로그인_비대면개설_신청완료','비대면개설_비로그인_신청완료'                                          \n"                       
              "                            )                                                                                          \n"                       
              "        GROUP BY DATE,STEP                                                                                             \n"                       
              "       ) B                                                                                                             \n"                       
              "    ON A.DATE=B.DATE                                                                                                   \n"                       
              "   AND A.DTL_CD_NM=B.STEP                                                                                              \n"
              "  LEFT OUTER JOIN                                                                                                      \n"
              "       (SELECT DATE AS DATE                                                                                            \n"
              "            , CASE WHEN ScreenName IN ('비로그인_비대면개설_메인'           , '비대면개설_비로그인_메인'           ) THEN '01단계_비로그인_비대면개설_메인'       \n"       
              "                   WHEN ScreenName IN ('비로그인_비대면개설_계좌선택'       , '비대면개설_비로그인_계좌선택'       ) THEN '02단계_비로그인_비대면개설_계좌선택'      \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_휴대폰본인인증' , '비대면개설_비로그인_휴대폰본인인증' ) THEN '03단계_비로그인_비대면개설_휴대폰본인인증'     \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_약관동의'       , '비대면개설_비로그인_약관동의'       ) THEN '04단계_비로그인_비대면개설_약관동의'      \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_고객정보입력'   , '비대면개설_비로그인_고객정보입력'   ) THEN '05단계_비로그인_비대면개설_고객정보입력'     \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_계좌인증'       , '비대면개설_비로그인_계좌인증'       ) THEN '06단계_비로그인_비대면개설_계좌인증'      \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_인증번호입력'   , '비대면개설_비로그인_인증번호입력'   ) THEN '07단계_비로그인_비대면개설_인증번호입력'     \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_신분증촬영'     , '비대면개설_비로그인_신분증촬영'     ) THEN '08단계_비로그인_비대면개설_신분증촬영'      \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_신분증촬영_결과', '비대면개설_비로그인_신분증촬영_결과') THEN '09단계_비로그인_비대면개설_신분증촬영_결과'    \n"
              "                   WHEN ScreenName IN ('비로그인_비대면개설_신청완료'       , '비대면개설_비로그인_신청완료'       ) THEN '10단계_비로그인_비대면개설_신청완료'      \n"
              "              ELSE ScreenName END AS STEP                                                             \n"    
              "            , SUM(VIEW_CNT) AS VCNT                                                                   \n"                                                                                                                                           
              "         FROM `hanwha-ga360.DT_STDO.MTS_SCRN_VW_CNT_DT`                                               \n"                  
              "        WHERE DATE='"+c_stdr_dt+"'                                                                    \n"               
              "          AND screenName IN (  '비로그인_비대면개설_메인','비대면개설_비로그인_메인'                               \n"                  
              "                             , '비로그인_비대면개설_계좌선택','비대면개설_비로그인_계좌선택'                         \n"                  
              "                             , '비로그인_비대면개설_휴대폰본인인증','비대면개설_비로그인_휴대폰본인인증'                \n"                  
              "                             , '비로그인_비대면개설_약관동의','비대면개설_비로그인_약관동의'                         \n"                  
              "                             , '비로그인_비대면개설_고객정보입력','비대면개설_비로그인_고객정보입력'                   \n"                  
              "                             , '비로그인_비대면개설_계좌인증','비대면개설_비로그인_계좌인증'                         \n"                  
              "                             , '비로그인_비대면개설_인증번호입력','비대면개설_비로그인_인증번호입력'                   \n"                  
              "                             , '비로그인_비대면개설_신분증촬영','비대면개설_비로그인_신분증촬영'                      \n"                  
              "                             , '비로그인_비대면개설_신분증촬영_결과','비대면개설_비로그인_신분증촬영_결과'              \n"                  
              "                             , '비로그인_비대면개설_신청완료','비대면개설_비로그인_신청완료'                         \n"                  
              "                            )                                                                         \n"                  
              "        GROUP BY DATE,STEP                                                                            \n"                  
              "       ) C                                                                                            \n"                  
              "    ON A.DATE=C.DATE                                                                                  \n"                  
              "   AND A.DTL_CD_NM=C.STEP                                                                             "
		)
		print ("QUERY : %s " % QUERY)
		query_job = client.query(QUERY).to_dataframe()    # API request
	except Exception as ex:
		print("insert_mts_nlgn_onln_new_acnt_dt 에러 발생 !!!!!! %s " % ex)
		endTime = time.time()
		etime=time.localtime(endTime)
		print ("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
		print ("수행시간 : %d 초" % (endTime-startTime))
		sys.exit(1)

if __name__ == "__main__" :
	startTime = time.time()
	stime=time.localtime(startTime)
	print ("mts_nlgn_onln_new_acnt_dt.py Job Start")
	print ("시작시간 : %04d-%02d-%02d %02d:%02d:%02d" % (stime.tm_year, stime.tm_mon, stime.tm_mday, stime.tm_hour, stime.tm_min, stime.tm_sec))

	#기준일자 YYYY-MM-DD 형식으로 변환
	stdr_dt = sys.argv[1]
	c_stdr_dt = datetime.strptime(stdr_dt, '%Y%m%d').strftime('%Y-%m-%d')
	
	if os.path.isfile('/home/dal/ga360/chk/complete_mts_scrn_vw_cnt_dt.'+sys.argv[1]+'.chk'):
		print ("chk file exits")
	else:
		print ("chk file not exits")	
		endTime = time.time()
		etime=time.localtime(endTime)
		print ("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
		print ("수행시간 : %d 초" % (endTime-startTime))
		sys.exit(1)
		
	#DELETE TABLE 호출
	delete_mts_nlgn_onln_new_acnt_dt(c_stdr_dt)
	#INSERT TABLE 호출
	insert_mts_nlgn_onln_new_acnt_dt(stdr_dt,c_stdr_dt)

	endTime = time.time()
	etime=time.localtime(endTime)
	print ("mts_nlgn_onln_new_acnt_dt.py Job End")
	print ("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
	print ("수행시간 : %d 초" % (endTime-startTime))
