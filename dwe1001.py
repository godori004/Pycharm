# -*- coding: utf-8 -*-
import sys
import time
from src.googleutil import bigquery

def bq_job(stdr_dt) :
	loop = 0
	while True:
		loop = loop+1
		print ("%d 번째 Try 수행" % loop)
		try:
			client = bigquery.Client()
			# Perform a query.e
			QUERY = ("WITH V_SSN_INFO AS                                                                                                   \n"
               "(                                                                                                                    \n"
               "SELECT DATE                                                                                                          \n"
               "     , CONCAT(fullVisitorId,'-',cast(visitId as string)) as cid                                                      \n"
               "     , visitNumber                                                                                                   \n"
               "     , TIMESTAMP_SECONDS(SAFE_CAST(visitStartTime AS INT64)+32400) AS t1                                             \n"
               "     , TIMESTAMP_SECONDS(SAFE_CAST(visitStartTime+IFNULL(totals.timeOnSite,0) AS INT64)+32400) AS t2                 \n"
               "     , IFNULL(totals.timeOnSite,0) as stime                                                                          \n"
               "     , MAX(case when cd.index=15 then cd.value ELSE NULL END) as CHNL_DTL_CD                                         \n"
               "     , MAX(case when cd.index=2 then cd.value ELSE NULL END) AS CUST_NO_ENC_CTNS                                     \n"
               "     , MAX(case when cd.index=3 then cd.value ELSE NULL END) AS ADID                                                 \n"
               "FROM `hanwha-ga360.191298234.ga_sessions_"+stdr_dt+"`, UNNEST(customDimensions) AS cd                                \n"
               "WHERE cd.index=15 or cd.index=2 or cd.index=3                                                                        \n"
               "GROUP BY DATE,cid,visitNumber,t1,t2,stime                                                                            \n"
               "HAVING CHNL_DTL_CD IN ('CC303','CC304')                                                                              \n"
               ")                                                                                                                    \n"
               "SELECT A.DATE                                                                                                        \n"
               "     , A.ADID                                                                                                        \n"
               "     , A.CID                                                                                                         \n"
               "     , A.visitNumber                                                                                                 \n"
               "     , FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', A.T1) AS START_TIME                                                     \n"
               "     , FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', A.T2) AS END_TIME                                                       \n"
               "     , A.STIME AS PGM_STAY_HR                                                                                        \n"
               "     , A.CUST_NO_ENC_CTNS                                                                                            \n"
               "     , B.CNVI_APP_USR_CLSF_CTNS                                                                                      \n"
               "     , CASE WHEN B.ISTL_PTH='(not set)' THEN NULL ELSE FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', T1) END AS PGM_ISTL_DTM \n"
               "     , CASE WHEN B.ISTL_PTH='(not set)' THEN NULL ELSE istl_pth END AS PGM_ISTL_URL_PATH_NM                          \n"
               "     , A.CHNL_DTL_CD                                                                                                 \n"
               "     , IFNULL(B.AUTH_DTL,'U') AS AUTH_DTL                                                                            \n"
               "     , B.CUST_NO_ENC_CTNS_TEMP                                                                                       \n"
               "  FROM V_SSN_INFO A                                                                                                  \n"
               " INNER JOIN                                                                                                          \n"
               "       (SELECT DATE                                                                                                  \n"
               "             , MAX(CONCAT(h.appInfo.appId,'_' ,h.appInfo.appVersion)) AS APPID                                       \n"
               "             , CONCAT(fullVisitorId,'-',cast(visitId as string)) as cid                                              \n"
               "             , MAX(h.appInfo.appInstallerId) AS istl_pth                                                             \n"               
               "             , IFNULL(MAX(CASE WHEN hcd.index=4 AND hcd.value='U' THEN NULL                                          \n"
               "                               WHEN hcd.index=4 AND hcd.value='1' THEN '3'                                           \n"
               "                               WHEN hcd.index=4 AND hcd.value='2' THEN '2'                                           \n"
               "                               WHEN hcd.index=4 AND hcd.value='3' THEN '1'                                           \n"
               "                               ELSE NULL END )                                                                       \n"
               "                         , 'U') AS CNVI_APP_USR_CLSF_CTNS                                                            \n"
               "             , MAX(CASE WHEN hcd.index=11 AND hcd.value='U' THEN NULL                                                \n"
               "                        WHEN hcd.index=11 THEN hcd.value                                                             \n"
               "                   ELSE NULL END) AS AUTH_DTL                                                                        \n"
               "             , MAX(case when hcd.index=24 then hcd.value ELSE NULL END) AS CUST_NO_ENC_CTNS_TEMP                     \n"
               "          FROM `hanwha-ga360.191298234.ga_sessions_"+stdr_dt+"`                                                      \n"
               "             , UNNEST(hits) AS h                                                                                     \n"
               "             , UNNEST(h.customDimensions) AS hcd                                                                     \n"
               "         GROUP BY date,cid                                                                                           \n"
               "       ) B                                                                                                           \n"
               "    ON A.DATE=B.DATE                                                                                                 \n"
               "   AND A.CID=B.CID                                                                                                   "
			)

			print ("QUERY : %s " % QUERY)

			query_job = client.query(QUERY).to_dataframe()    # API request
			query_job.to_csv('C:/TEMP/ga360_smartm_dwe1001.csv.'+stdr_dt, header=False, index=False, encoding='utf-8')
			break
		except Exception as ex:
			print("Bigquery 에러 발생 !!!!!! %s " % ex)
			if loop == 4:
				print ("Error Occurred, This Job is quite")
				endTime = time.time()
				etime=time.localtime(endTime)
				print ("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
				print ("수행시간 : %d 초" % (endTime-startTime))
				sys.exit(1)
			time.sleep(1800)

if __name__ == "__main__" :
	startTime = time.time()
	stime=time.localtime(startTime)
	print ("dwe1001.py Job Start")
	print ("시작시간 : %04d-%02d-%02d %02d:%02d:%02d" % (stime.tm_year, stime.tm_mon, stime.tm_mday, stime.tm_hour, stime.tm_min, stime.tm_sec))
	bq_job("20200302")
	endTime = time.time()
	etime=time.localtime(endTime)
	print ("dwe1001.py Job End")
	print ("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
	print ("수행시간 : %d 초" % (endTime-startTime))

