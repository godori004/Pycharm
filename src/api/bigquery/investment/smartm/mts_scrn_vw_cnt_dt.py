# -*- coding: utf-8 -*-
# CREATER : 호이춘

import sys
import os
import time
from src.googleutil import bigquery
from datetime import datetime


def touch(fname, times=None) :
	fhandle = open(fname,'a')
	try:
		os.utime(fname, times)
	finally:
		fhandle.close()

def delete_mts_scrn_vw_cnt_dt(c_stdr_dt) :
	try:
		client = bigquery.Client()
		# Perform a query.
		QUERY = ("DELETE FROM `hanwha-ga360.DT_STDO.MTS_SCRN_VW_CNT_DT` WHERE DATE='"+c_stdr_dt+"'")
		print ("QUERY : %s " % QUERY)
		query_job = client.query(QUERY).to_dataframe()    # API request
		
	except Exception as ex:
		print("delete_mts_scrn_vw_cnt_dt 에러 발생 !!!!!! %s " % ex)		
		endTime = time.time()
		etime=time.localtime(endTime)
		print ("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
		print ("수행시간 : %d 초" % (endTime-startTime))
		sys.exit(1)

def insert_mts_scrn_vw_cnt_dt(stdr_dt,c_stdr_dt) :
	try:
		client = bigquery.Client()
		# Perform a query.
		QUERY = ("INSERT INTO `hanwha-ga360.DT_STDO.MTS_SCRN_VW_CNT_DT`                                        \n"
		         "SELECT PARSE_TIMESTAMP('%Y%m%d', A.DATE) AS DATE                                             \n"
             "     , CONCAT(A.fullVisitorId,'-',cast(A.visitId as string)) AS SID                          \n"
             "     , h.appInfo.screenName as screenName                                                    \n"
             "     , COUNT(*) AS VIEW_CNT                                                                  \n"
             "  FROM `hanwha-ga360.191298234.ga_sessions_"+stdr_dt+"` A                                  \n"
             "     , (SELECT DATE                                                                          \n"
             "             , CONCAT(fullVisitorId,'-',cast(visitId as string)) as SID                      \n"
             "             , MAX(case when cd.index=15 then cd.value ELSE NULL END) as CHNL_DTL_CD         \n"
             "          FROM `hanwha-ga360.191298234.ga_sessions_"+stdr_dt+"`, UNNEST(customDimensions) AS cd \n"
             "         WHERE cd.index=15                                                                   \n"
             "         GROUP BY DATE,SID                                                                   \n"
             "        HAVING CHNL_DTL_CD IN ('CC303','CC304'))B                                            \n"
             "     , UNNEST(hits) AS h                                                                     \n"             
             "  WHERE A.DATE=B.DATE                                                                        \n"
             "    AND B.SID = CONCAT(A.fullVisitorId,'-',cast(A.visitId as string))                        \n"
             "    AND h.type='APPVIEW'                                                                     \n"
             "  GROUP BY A.DATE,SID, screenName                                                            "
		)
		print ("QUERY : %s " % QUERY)
		query_job = client.query(QUERY).to_dataframe()    # API request
	except Exception as ex:
		print("insert_mts_scrn_vw_cnt_dt 에러 발생 !!!!!! %s " % ex)
		endTime = time.time()
		etime=time.localtime(endTime)
		print ("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
		print ("수행시간 : %d 초" % (endTime-startTime))
		sys.exit(1)

if __name__ == "__main__" :
	startTime = time.time()
	stime=time.localtime(startTime)
	print ("mts_scrn_vw_cnt_dt.py Job Start")
	print ("시작시간 : %04d-%02d-%02d %02d:%02d:%02d" % (stime.tm_year, stime.tm_mon, stime.tm_mday, stime.tm_hour, stime.tm_min, stime.tm_sec))

	#기준일자 YYYY-MM-DD 형식으로 변환
	stdr_dt = sys.argv[1]
	c_stdr_dt = datetime.strptime(stdr_dt, '%Y%m%d').strftime('%Y-%m-%d')
	
	#DELETE TABLE 호출
	delete_mts_scrn_vw_cnt_dt(c_stdr_dt)
	#INSERT TABLE 호출
	insert_mts_scrn_vw_cnt_dt(stdr_dt,c_stdr_dt)

	endTime = time.time()
	etime=time.localtime(endTime)
	print ("mts_scrn_vw_cnt_dt.py Job End")
	
	touch('/home/dal/ga360/chk/complete_mts_scrn_vw_cnt_dt.'+stdr_dt+'.chk')
  
	print ("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
	print ("수행시간 : %d 초" % (endTime-startTime))
