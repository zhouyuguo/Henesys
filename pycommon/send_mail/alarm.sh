#!/bin/sh

cwd=`dirname $0`

#EMAILTo="yanyi.wu@alibaba-inc.com, panfeng.pan@aliyun-inc.com, xing.rao@alibaba-inc.com, xiaoxun.zhang@alibaba-inc.com"
#EMAILTo="wuping.li@alibaba-inc.com, liuhang.cheng@alibaba-inc.com, sheng.feng@alibaba-inc.com, haihong.xiahh@alibaba-inc.com, xue.wangxue@alibaba-inc.com, allen.wang@aliyun-inc.com, daniel.tangc@alibaba-inc.com, xing.rao@alibaba-inc.com, panfeng.pan@aliyun-inc.com, xiaoxun.zhang@alibaba-inc.com, jiqing.liu@aliyun-inc.com, xiaoyu.leng@aliyun-inc.com, guorui.xiaogr@alibaba-inc.com, jose.wangzy@alibaba-inc.com, yeguo.wu@alibaba-inc.com, tao.li@alibaba-inc.com, sheng.qiang@alibaba-inc.com, qing.tan@alibaba-inc.com, hongjie.wu@alibaba-inc.com, yanyi.wu@alibaba-inc.com, jingcheng.lijc@aliyun-inc.com"
SMTPServer="smtp.ops.aliyun-inc.com"


Subject="$1"" ["`/bin/date +%F" "%T`"]"
Emailbody="$2"
File="$3"
if [ "$4" == NULL ]; then
        $cwd/sendEmail -s "${SMTPServer}" -f "${EMAILFrom}" -t "${EMAILTo}" -u "${Subject}"  -m "${Emailbody}"
        exit 0
else
        $cwd/sendEmail -s "${SMTPServer}" -f "${EMAILFrom}" -t "${EMAILTo}" -u "${Subject}"  -m "${Emailbody}" -a "${File}" -o message-charset="utf-8"
        exit 0
fi
