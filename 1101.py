# -*- coding: utf-8 -*-
import sys
import time
from google.cloud import bigquery
from google.cloud import storage


def bq_job(stdr_dt):
    loop = 0
    while True:
        loop = loop + 1
        print("%d 번째 Try 수행" % loop)
        try:
            client = bigquery.Client()
            # Perform a query.
            QUERY = (
                        "WITH V_SSN_INFO AS                                                                                                   \n"
                        "(                                                                                                                    \n"
                        "SELECT DATE                                                                                                          \n"
                        "     , CONCAT(fullVisitorId,'-',cast(visitId as string)) as SID                                                      \n"
                        "     , visitNumber                                                                                                   \n"
                        "     , TIMESTAMP_SECONDS(SAFE_CAST(visitStartTime AS INT64)+32400) AS t1                                             \n"
                        "     , TIMESTAMP_SECONDS(SAFE_CAST(visitStartTime+IFNULL(totals.timeOnSite,0) AS INT64)+32400) AS t2                 \n"
                        "     , IFNULL(totals.timeOnSite,0) as stime                                                                          \n"
                        "     , MAX(case when cd.index=15 then cd.value ELSE NULL END) as CHNL_DTL_CD                                         \n"
                        "     , MAX(case when cd.index=2 then cd.value ELSE NULL END) AS CUST_NO_ENC_CTNS                                     \n"
                        "     , MAX(case when cd.index=3 then cd.value ELSE NULL END) AS ADID                                                 \n"
                        "FROM `hanwha-ga360.191298234.ga_sessions_" + stdr_dt + "`, UNNEST(customDimensions) AS cd                                \n"
                                                                                "WHERE cd.index=15 or cd.index=2 or cd.index=3                                                                        \n"
                                                                                "GROUP BY DATE,SID,visitNumber,t1,t2,stime                                                                            \n"
                                                                                "HAVING CHNL_DTL_CD IN ('CC303','CC304')                                                                              \n"
                                                                                ")                                                                                                                    \n"
                                                                                " SELECT B.DATE                                                                                                                                    \n"
                                                                                "      , A.ADID                                                                                                                                    \n"
                                                                                "      , B.SID                                                                                                                                     \n"
                                                                                "      , B.hitNumber                                                                                                                               \n"
                                                                                "      , B.SCRN_ID                                                                                                                                 \n"
                                                                                "      , B.screenName                                                                                                                              \n"
                                                                                "      , FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', B.T1) AS CNN_DTM                                                                                    \n"
                                                                                "      , IFNULL(GREATEST( CASE WHEN LEAD(B.T1) OVER (PARTITION BY B.DATE,B.SID ORDER BY B.hitNumber) IS NULL THEN TIMESTAMP_DIFF(B.T2,B.T1,SECOND) \n"
                                                                                "                  ELSE TIMESTAMP_DIFF(LEAD(B.T1) OVER (PARTITION BY B.DATE,B.SID ORDER BY B.hitNumber),B.T1,SECOND)                               \n"
                                                                                "                  END                                                                                                                             \n"
                                                                                "                , 0),0) AS STAY_SCND                                                                                                              \n"
                                                                                "      , A.CHNL_DTL_CD                                                                                                                             \n"
                                                                                "     FROM V_SSN_INFO A                                                                                                                            \n"
                                                                                "  INNER JOIN                                                                                                                                      \n"
                                                                                "        (SELECT DATE                                                                                                                              \n"
                                                                                "              , CONCAT(fullVisitorId,'-',CAST(visitId AS STRING)) AS SID                                                                          \n"
                                                                                "              , h.hitNumber AS hitNumber                                                                                                          \n"
                                                                                "              , TIMESTAMP_SECONDS(SAFE_CAST(visitStartTime+h.TIME/1000 AS INT64)+32400) AS T1                                                     \n"
                                                                                "              , TIMESTAMP_SECONDS(SAFE_CAST(visitStartTime+totals.timeOnScreen AS INT64)+32400) AS T2                                             \n"
                                                                                "              , MAX(CONCAT(h.appInfo.appId,'_' ,h.appInfo.appVersion)) AS APPID                                                                   \n"
                                                                                "              , h.appInfo.screenName as screenName                                                                                                \n"
                                                                                "              , MAX(IF(hcd.index=19, hcd.value, NULL)) SCRN_ID                                                                                    \n"
                                                                                "           FROM `hanwha-ga360.191298234.ga_sessions_" + stdr_dt + "`, UNNEST(hits) AS h, UNNEST(h.customDimensions) as hcd                            \n"
                                                                                                                                                   "          WHERE h.type='APPVIEW'                                                                                                                  \n"
                                                                                                                                                   "          GROUP BY DATE, SID,hitNumber,T1,T2,screenName                                                                                           \n"
                                                                                                                                                   "        ) B                                                                                                                                       \n"
                                                                                                                                                   "     ON A.DATE=B.DATE                                                                                                                             \n"
                                                                                                                                                   "    AND A.SID=B.SID                                                                                                                               "
                        )

            print("QUERY : %s " % QUERY)

            query_job = client.query(QUERY).to_dataframe()  # API request
            query_job.to_csv('C:/Temp/ga360_smartm_dwe1101.csv.' + stdr_dt, header=False,
                             index=False, encoding='utf-8')
            break
        except Exception as ex:
            print("Bigquery 에러 발생 !!!!!! %s " % ex)
            if loop == 4:
                print("Error Occurred, This Job is quite")
                endTime = time.time()
                etime = time.localtime(endTime)
                print("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (
                etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
                print("수행시간 : %d 초" % (endTime - startTime))
                sys.exit(1)
            time.sleep(1800)

def strg_job(stdr_dt):
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('hanwhawm')
        blob = bucket.blob('smartm/ga360_smartm_dwe1101.csv.' + stdr_dt)
        blob.upload_from_filename('C:/Temp/ga360_smartm_dwe1101.csv.' + stdr_dt)
    except Exception as ex:
        print("Storage 에러 발생 !!!!!! %s " % ex)
        endTime = time.time()
        etime = time.localtime(endTime)
        print("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (
        etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
        print("수행시간 : %d 초" % (endTime - startTime))
        sys.exit(1)


if __name__ == "__main__":
    startTime = time.time()
    stime = time.localtime(startTime)
    print("dwe1101.py Job Start")
    print("시작시간 : %04d-%02d-%02d %02d:%02d:%02d" % (
    stime.tm_year, stime.tm_mon, stime.tm_mday, stime.tm_hour, stime.tm_min, stime.tm_sec))
    bq_job('20200319')
    strg_job('20200319')
    endTime = time.time()
    etime = time.localtime(endTime)
    print("dwe1101.py Job End")
    print("종료시간 : %04d-%02d-%02d %02d:%02d:%02d" % (
    etime.tm_year, etime.tm_mon, etime.tm_mday, etime.tm_hour, etime.tm_min, etime.tm_sec))
    print("수행시간 : %d 초" % (endTime - startTime))

