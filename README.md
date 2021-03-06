`MSZ_SKLCC` 成品质检系统版本更新记录
=================
@(项目工作笔记)[MSZ_SJKCC|版本迭代记录]

------------
>[@xuweitao](https://github.com/pyxuweitao/MSZ_SKLCC "code in github:MSZ_SKLCC")
>
<strong>在2014年6月4日凌晨发行了β版本,并正式进入公测阶段:</strong>
<br>
<strong>9月2日通过验收，并更新项目名称为`MSZ_SKLCC`
</br>
*以下是更新记录：* 
</br>

<table>
<tr>
<td style="width:150px">日期</td><td style="width:1000px"> 更新内容</td><td style = "width:80px">涉及文件</td>

</tr>

<tr>
<td>2016-03-31</br><h2>v2.4.1</h2>
</td>
<td> 
<ul>
<li>工艺员出现尺码多输空格情况，为了防止匹配不上二捡处对尺码采取LIKE模糊匹配</li>
</td>
<td>
<ul>
<li>views.py</li>
</ul>
</td>
</tr>

<tr>
<td>2016-03-22</br><h2>v2.4.0</h2>
</td>
<td> 
<ul>
<li>提交超时疵点翻倍的BUG修复</li>
<li>疵点构成增加批次过滤条件</li>
</td>
<td>
<ul>
<li>views.py</li>
<li>pie_chart.html</li>
<li>chart.py</li>
<li>dataentry.js</li>
</ul>
</td>
</tr>

</tr>
<tr>
<td>2015-05-11</br><h2>v2.3.6</h2>
</td>
<td> 
<ul>
<li>一检、二检报表审批界面增加时间过滤条件</li>
<li>搜索框响应实体键盘的事件添加</li>
</td>
<td>
<ul>
<li>views.py</li>
<li>choose_check.html</li>
<li>choose_recheck_check.html</li>
<li>dataentry.js</li>
</ul>
</td>
</tr>
<tr>
<tr>
<td>2015-05-09</br><h2>v2.3.5</h2>
</td>
<td> 
<ul>
<li>修复一检输入框定位到前部输入时自动添加到最后的BUG</li>
<li>修复抽验工时工价统计表与抽验员平均效率汇总工时计算方式统一</li>
<li>一检审批编码问题修复</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>utilitys.py</li>
<li>forms.py</li>
<li>部分html</li>
<li>dataentry.js</li>
</ul>
</td>
</tr>
<tr>
<tr>
<td>2015-05-06</br><h2>v2.3.4</h2>
</td>
<td> 
<ul>
<li>因为所有检验员配备了小键盘，故去掉了界面上小键盘的显示</li>
<li>修复意见审批界面表格数据没有过滤的BUG</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>部分html</li>
<li>recheck.js</li>
</ul>
</td>
</tr>
<tr>
<td>2015-04-29</br><h2>v2.3.3</h2>
</td>
<td> 
<ul>
<li>实现了前台提交失败的条码写入cookie进行检查，进一步保证提交数量准确</li>
<li>根据一检检验员需求增加了“质量用的”快捷输入</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>部分html</li>
<li>部分js</li>
</ul>
</td>
</tr>
<tr>
<tr>
<td>2015-04-16</br><h2>v2.3.2</h2>
</td>
<td> 
<ul>
<li>一检提交失败提示框取消自动提交</li>
<li>一检提交成功弹出的提示框增加当前提交的批次检验总数</li>
<li>修复返修活检验中出现的重复记录问题</li>
<li>二检审批增加不通过退回可修改功能</li>
<li>二检审批增加抽验员列</li>
<li>抽验工时工价表去除二检未提交的数据</li>
<li>工艺测量表单中尺码根据工艺员录入顺序固定</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>measure.py</li>
<li>utilitys.py</li>
<li>部分html</li>
<li>部分js</li>
</ul>
</td>
</tr>
<tr>
<td>2015-04-12</br><h2>v2.3.1</h2>
</td>
<td> 
<ul>
<li>小键盘实现删除光标精确位置前的内容</li>
<li>尺寸测量审批因数据统计删去全部提交按钮</li>
<li>一检表单明细界面显示包含的条码信息</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>measure.py</li>
<li>utilitys.py</li>
<li>部分html</li>
<li>部分js</li>
</ul>
</td>
</tr>
<tr>
<tr>
<td>2015-04-09</br><h2>v2.3</h2>
</td>
<td> 
<ul>
<li>款号通过批号截取字符串的问题修正，改为数据库查询</li>
<li>网络状况不良提示关不掉的BUG修正</li>
<li>一检页面右上角提示框新增出现错误可以重试提交的功能</li>
<li>工艺测量中公差上限改为3</li>
<li>抽验工时工价表中对检验工序的匹配条件改为qcbz=1，包括效率和总工时计算也进行了修正</li>
<li>工艺测量审批默认日期范围改为一个月</li>
<li>部位测量审批新增查询功能</li>
<li>抽验工时工价表中新增一列（套灯模工时），套灯模工时也纳入总工时</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>measure.py</li>
<li>utilitys.py</li>
<li>forms.py</li>
<li>部分html</li>
<li>部分js</li>
<li>SQL脚本</li>
</ul>
</td>
</tr>
<tr>
<td>2015-04-01</br><h2>v2.2.1</h2>
</td>
<td> 
<ul>
<li>优化脏读查询，防止因为数据库上锁而出现网络状况不良</li>
<li>部位测量提交之后数据与部位不对应的情况修复</li>
<li>一检提交提示框关不掉的BUG修复</li>
<li>工艺测量部位新增款的时候必须点其他选项才能增加部位的BUG修复</li>
<li>一检和二检的正负号重复出现的BUG修复</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>measure.py</li>
<li>部分html</li>
<li>部分js</li>
</ul>
</td>
</tr>
<td>2015-03-30</br><h2>v2.2</h2>
</td>
<td> 
<ul>
<li>检验员返修活记录表检验数量全部为0的BUG修复</li>
<li>一检录入界面数据没有添加便提交的提示</li>
<li>一检录入界面数据没有提交便转移页面的提示</li>
<li>一检提交失败提示长时间悬浮</li>
<li>二检提交速度优化为原来的1/17</li>
<li>工艺测量增加正负公差</li>
<li>返修活检验实现链式补录</li>
<li>返修活检验如果存在疵点则默认不通过</li>
<li>二检尺寸测量获取流水号的BUG修复</li>
<li>二检部位测量录入过程优化</li>
<li>检验部分部位测量提交过程优化</li>
<li>修改错误日志文件写入方法</li>
<li>查看汇总修活数量和明细不一致的BUG修复</li>
<li>一检提交错误的BUG修复</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>measure.py</li>
<li>urls.py</li>
<li>utilitys.py</li>
<li>forms.py</li>
<li>部分html</li>
<li>部分js</li>
<li>SQL脚本</li>
</ul>
</td>
</tr>
<tr>
<td>2015-03-17</br><h2>v2.1.3</h2>
</td>
<td> 
<ul>
<li>检验员部位测量审批页面数据刷新的BUG修复</li>
<li>工艺测量中部位测量审批增添时间过滤，增添表头信息：审批员、审批时间、状态</li>
<li>二检尺寸录入增加一组尺寸之后，使用回车可以在单元格内顺序向下移动</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>measure.py</li>
<li>measure_check.html</li>
<li>measure_check_recheck.html</li>
<li>部分js</li>
</ul>
</td>
</tr>
<tr>
<td>2015-03-16</br><h2>v2.1.2</h2>
</td>
<td> 
<ul>
<li>一检中工序增添"花边"、"肩带"，对应"花边组"、"肩带组"</li>
<li>工艺测量的部位测量页面增加显示该单审批员和审批时间信息</li>
<li>添加尺寸测量的公差不能为空的验证</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>measure.py</li>
<li>measure_size_set.html</li>
<li>SQL脚本</li>
</ul>
</td>
</tr>

<tr>
<td>2015-03-14</br><h2>v2.1.1</h2>
</td>
<td> 
<ul>
<li>工艺部位维护提交结果提示与实际提交结果不一致的BUG修复</li>
<li>工艺录入的出现错位或者数据丢失的问题修复</li>
<li>一检条码检验是否属于当前录入款的提示修正</li>
<li>工艺录入无法使用方向键移动的BUG修复</li>
<li>报数录入提交错误的BUG修复</li>
<li>增加检验员部位测量录入数据有误的高亮提示</li>
<li>二检部位测量审批页面查询出现一检的数据的BUG修复</li>
<li>优化一检疵点录入提交速度</li>
<li>所有的日期选择都增添默认值</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>utilitys.py</li>
<li>measure.py</li>
<li>部分html</li>
<li>sql脚本</li>
<li>js文件</li>
</ul>
</td>
</tr>

<tr>
<td>2015-03-12</br><h2>v2.1</h2>
</td>
<td> 
<ul>
<li>个人信息页面一检漏验率历史信息查询BUG修复</li>
<li>扫码登录错误捕捉</li>
<li>部位测量审批结果出现错位问题的修复</li>
<li>一检工序中添加粘合和粘合组工序</li>
<li>一检尺寸测量小键盘挡住输入框的BUG修复</li>
<li>一检尺寸测量冻结行的功能实现</li>
<li>一检半检工序变为醒目的红色</li>
<li>部位测量页面可以用方向键控制输入框</li>
<li>二检复检的时候不需要测量尺寸</li>
<li>增加一检提交不同批次时候的提示</li>
<li>一检提交改为异步模式以加快提交速度</li>
<li>工艺测量中部位测量增加原录入工艺员的姓名</li>
<li><strong>实现工艺测量的审批过程,不通过可退回重新录入</strong></li>
<li>控制一检或二检只可以录入通过工艺审批的部位测量数据</li>
<li>检验员部位测量的对称误差数据显示不对齐的BUG修复</li>
<li>检验员部位测量的审批页面班组名称重复的BUG修复</li>
<li>二检导航栏透明BUG修复</li>
<li>一检提交增加浮点数验证</li>
<li>尺寸测量审批增加日期和批号条件进行过滤</li>
<li>审批页面错位</li>
<li>一检尺寸测量提交删除旧数据的BUG修复</li>
<li>尺寸测量审批数据统计同尺码不同批次归并的BUG修复</li>
<li>工艺员部位测量页面增加复制某款所有尺码测量数据功能简化工艺员录入过程</li>
<li>增加权限工艺测量审批和相应的权限控制</li>
<li>对一检和二检的部位测量审批中过滤的数据做出了区分</li>
<li>部位测量尺码过多增添尺码时下方滚动条自动向右滚动</li>
<li>二检提交不上的BUG修复</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>utilitys.py</li>
<li>measure.py</li>
<li>urls.py</li>
<li>部分html</li>
<li>sql脚本</li>
<li>js文件</li>
</ul>
</td>
</tr>

<tr>
<td>2015-03-05</br><h2>v2.0</h2>
</td>
<td> 
<ul>
<li>抽验员平均效率汇总报表的平均效率计算方法修正</li>
<li>返修活检验记录汇总报表无数据的BUG修复</li>
<li>阶段返修记录表剔除非线上检验人员名单</li>
<li><strong>二检尺寸测量正式测试版本发布</strong></li>
<li>二检尺寸测量页面布局设计优化</li>
<li>二检尺寸测量用户输入交互设计优化</li>
<li>一检尺寸测量界面优化</li>
<li>二检控制录入提交件数限制为样本量的10%</li>
<li>数字键盘输入优化：无需每次保存都点击对勾</li>
<li>增加报表form13:工艺测量汇总，可根据工艺员姓名和时间段过滤录入过部位的款号列表</li>
<li>工艺测量中部位测量查询出的部位顺序保持与录入一致</li>
<li>工艺测量中部位测量，公差、对称误差增加下拉框和步进功能以方便录入</li>
<li>为每位工艺员增加了常有部位编辑的维护标签页，可以在部位测量页面快速添加尺码</li>
<li>数字键盘输入优化：无需每次保存都点击对勾</li>
<li>部位测量页面选中测量种类之后部位下拉列表只显示当前选择种类</li>
<li>目前拥有一检审批权限和二检审批权限的员工均可通过“部位测量审批”页面查看检验员部位测量的内容</li>
<li>工艺测量中的部位测量页面字体、表格等宽度调整，优化显示效果</li>
<li>一检产量汇总表剔除非检验人员的汇总信息</li>
<li>一检录入工序和明细表工序不一致的BUG修复</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>utilitys.py</li>
<li>measure.py</li>
<li>部分html</li>
<li>sql脚本</li>
<li>js文件</li>
</ul>
</td>
</tr>

<tr>
<td>2015-02-10</td>
<td> 
<ul>
<li>配置APACHE启用前端浏览器终端的静态资源缓存来提高性能</li>
<li>优化一检扫描条码查询代码，提高查询效率</li>
<li>修复重复扫描条码的BUG</li>
<li>增添新功能：部位测量增量输入</li>
<li>部位测量默认全部打钩</li>
<li>数据库为简化一检扫描条码查询，增加函数get_check_info_by_barcode，get_produce_info_by_barcode，get_update_info_xml，增加触发器update_sklcc_measure_record_when_commit_res,增加存储过程pick_up_data_sync_sklcc_info_table_record</li>
<li>优化一检录入条码时查询逻辑，减少表连接和不必要的条件判断，防止数据库死锁产生</li>
<li>优化缓存设置，修复数据不准的BUG（缓存导致）
<li>优化尺寸测量的录入逻辑，转移到提交处进行</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>utilitys.py</li>
<li>measure.py</li>
</ul>
</td>
</tr>

<tr>
<td>2015-02-05</td>
<td> 
<ul>
<li>修正了一检报表明细无法查看的BUG</li>
<li>优化一检数据提交速度，经测试提高近8倍左右（496000>>>58000）</li>
<li>数据库为简化查询，增加函数get_questioncode_by_no，get_questiontype_by_no，get_workname_by_worklineno_and_barcode，get_check_type_by_check_id，get_totalnumber_by_serialno，增加触发器update_sklcc_table_when_insert</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>utilitys.py</li>
</ul>
</td>
</tr>

<tr>
<td>2015-02-03</td>
<td> 
<ul>
<li>用户个人信息查询BUG修复</li>
<li>修正了检验员平均效率没有数据的BUG</li>
<li>返修率汇总表查询数据时候显示错位的修正</li>
<li>优化了后台查看汇总和报表审批的代码，修复了报表审批报表明细查询的BUG</li>
<li>添加了数据库根据系统配置获取离当前时间为sklcc_config(days)天的时间字符串函数get_date_before_config_days</li>
<li>所有BDDMS_MSZ数据库查询加上WITH(NOLOCK)选项防止数据库锁定</li>
</ul>
</td>
<td>
<ul>
<li>views.py</li>
<li>utilitys.py</li>
</ul>
</td>
</tr>


<tr>
<td>2014-09-02</br><h2>v1.0</h2></td>
<td><ul>
<li>修复一检录入BUG
<li>腾讯通发送定时通知功能实现，并添加配置文件。
<li>修复刷条码登录管理员账号的漏洞
<li>建立并迁移本系统数据库SKLCC
<li>重新整理项目文件，并正式更新项目名称为MSZ_SKLCC
</ul></td>
<td><ul>
<li>SKLCC_database.sql
<li>MSZ_SKLCC所有项目文件
</ul></td>

<tr>
<td>2014-09-01</td>
<td><ul>
<li>刷条码登录的BUG修复
<li>二检查看汇总报表汇总的BUG修复
</ul></td>
<td><ul>
<li>views.py
<li>forms.py
<li>dataentry_js.js
<li>urls.py
<li>dataentry.html
<li>所有以table为前缀的html文件
</ul></td>

<tr>
<td>2014-08-29</td>
<td><ul>
<li>饼状图数据查询实现和放大
<li>导航栏图表报表名称修改
<li>奖罚表表头修改和数字零隐藏
<li>添加新报表平均效率汇总
<li>权限管理增加用户员工工号和账户名默认同步输入
<li>疵点录入和报数录入界面实现扫条码登录
<li>权限管理界面系统配置增加扫描登录开关和实际工作工时配置
<li>增加饼状图和抽验员平均效率汇总报表的权限控制
<li>增加数据表sklcc_effciency存储抽验员每日工作效率
</ul></td>
<td><ul>
<li>sklcc_authority.sql
<li>views.py
<li>forms.py
<li>chart.py
<li>dataentry_js.js
<li>management.html
<li>number_off.html
<li>management_function.js
<li>pie_chart.html
<li>table_check_miss.html
<li>table_reckeck_efficiency.html
</ul></td>

<tr>
<td>2014-08-27</td>
<td><ul>
<li>柱状图相关功能实现
<li>报数录入进入时自动刷新批次号
<li>报数录入搜索功能实现
<li>柱状图、一检查量汇总表、返修活检验记录汇总添加权限控制
</ul></td>
<td><ul>
<li>sklcc_authority.sql
<li>views.py
<li>forms.py
<li>chart.py
<li>management.html
<li>base.html
<li>number_off.html
<li>bar_question_chart.html
</ul></td>

<tr>
<td>2014-08-26</td>
<td><ul>
<li>数据统计添加报表：一检产量汇总表
<li>部分报表名称修正
<li>报表整合报数录入数据
<li>一检、二检返修活检验录入疵点和审核功能实现
<li>报数录入版块实现
<li>报数录入数据表整合进入一检查看汇总
<li>一检录入权限放开
<li>权限管理界面添加报数录入工序列表，实现检验工序参数化
<li>新增数据表:sklcc_check_type，存放检验工序类型
</ul></td>
<td><ul>
<li>views.py
<li>forms.py
<li>pad.py
<li>chart.py
<li>url_dataentry.html
<li>management.html
<li>daliy_return_check.html
<li>number_off.html
<li>management_function.js
<li>dataentry.js
<li>recheck.js
<li>select2.css
<li>select2.js
<li>...涉及文件数较多,未全部列出
</ul></td>


<tr>
<td>2014-08-21</td>
<td><ul>
<li>抽验录入界面根据组别号刷新批次的BUG修复
<li>一检查看汇总显示非本人报表的BUG
<li>奖惩汇总报表可以在系统配置页面进行配置
<li>一检录入中工序对应的责任人可以通过输入工号添加
<li>优化了后台代码的可维护性
<li>抽验界面刷新员工姓名将属于所选组别的员工排在最上边
</ul></td>
<td><ul>
<li>table_check_miss.html
<li>management.html
<li>dataentry_js.js
<li>views.py
<li>forms.py
<li>urls.py
<li>sklcc_config.sql
</ul></td>

<tr>
<td>2014-08-07</td>
<td><ul>
<li>数据库增加报表权限
<li>抽验界面增加多选提交和提交全部功能
<li>抽验工时工价汇总表增加工号
<li>用户信息增加已提交表单查询
<li>数据统计中历史记录报表显示拥有权限所有组别的数据
<li>增加抽验工时工价表的权限控制
<li>优化一检界面疵点工序选择机制
<li>修复报表修改保存的BUG
<li>增加电子屏显示:报警和固定时间点发送消息
<li>修复抽验捋肩带显示的BUG
<li>一检和二检录入界面优化
<li>修复一检查看汇总无法查看已提交只读表的BUG
</ul></td>
<td><ul>
<li>views.py
<li>forms.py
<li>urls.py
<li>base.html
<li>management.html
<li>table_chcek_miss.html
<li>manage_function.js
<li>dataentry.html
<li>dataentry_js.js
<li>增加抽验报表权限.sql
<li>EQ_IM_TIME.py
<li>EQOPENCLOSE.py
<li>EQSEND.py
<li>MSZ_EQ.exe
<li>EQ2008_DLL.dll
<li>EQ2008_Dll_Set.ini
<li>EQ_open_close_all.dll
<li>EQ_open_close.dll
<li>groupscreen.txt
</tr>

<td>2014-07-31</td>
<td><ul>
<li>取消报表查询默认时间
<li>配置页面增添肩带工价
<li>配置页面增添肩带工时
<li>权限管理界面增添奖惩规则管理
<li>增添抽验工时工价汇总表
<li>一检界面显示调整
<li>修复修改二检组别顺序的BUG
<li>奖罚汇总套用文胸和小裤公式
</ul></td>
<td><ul>
<li>views.py
<li>forms.py
<li>daily_return_check.html
<li>management.html
<li>management_function.js
<li>table_rechcek_status.html
<li>urls.py
</ul></td>


<tr>
<td>2014-07-30</td>
<td><ul>
<li>修复返修活检验请求的BUG
<li>权限管理可以批量修改权限
<li>报表检验员返修活汇总修正
<li>报表相关岗位品质奖罚修正
<li>返修活检验页面实现翻页
<li>修复捋肩带报表姓名显示的BUG
</ul></td>
<td><ul>
<li>views.py
<li>forms.py
<li>daily_return_check.html
<li>management.html
<li>management_function.js
<li>table_quality_check.html
<li>table_read_only.html
<li>table_haven_submitted.html
<li>urls.py
</ul></td>


<tr>
<td>2014-07-29</td>
<td><ul>
<li>修复了一检写入错误审批时间的BUG
<li>修复了一检录入无疵点记录提交失败的BUG
<li>修复了捋肩带只传入捋肩带总条数的出现的BUG
<li>捋肩带可以查看明细
<li>增加报表：品质考核表-检验员返修活汇总
<li>增加报表：品质考核表-检验员返修率汇总
<li>报表添加合计一栏
<li>增加报表：阶段致命不良汇总
<li>增加报表：相关岗位品质奖罚汇总
</ul></td>
<td><ul>
<li>base.html
<li>recheck.html
<li>recheck.js
<li>table_bald_history.html
<li>table_check_miss.html
<li>table_quality_check.html
<li>table_read_only.html
<li>table_haven_submitted.html
<li>views.py
<li>dataentry.html
<li>forms.py
<li>urls.py
</ul></td>


<tr>
<td>2014-07-25</td>
<td><ul>
<li>抽验捋肩带流程重新设计
<li>捋肩带数据表重新设计
<li>抽验清款不显示批号的BUG
<li>抽验界面组别重复显示的BUG
<li>返修活检验功能实现
<li>抽验界面根据分辨率显示调整
<li>个人信息界面添加捋肩带和漏验明细显示
<li>疵点快速搜索小键盘输入结束自动清零
<li>一检、二检小键盘加清空按钮
<li>优化了一检记录提交时的性能
</ul></td>
<td><ul>
<li>sklcc_recheck_bald_new.sql
<li>forms.py
<li>urls.html
<li>management.html
<li>table_haven_submitted.html
<li>table_stage_repair.html
<li>function_management.js
<li>增添daily_return_check.html
<li>recheck.js
<li>recheck.html
<li>dataentry.js
<li>daily_return_check.html
</ul></td>


<tr>
<td>2014-07-23</td>
<td><ul>
<li>抽验样本量可以等于批量
<li>抽验界面增添批号过滤时间选项
<li>抽验界面一检检验员不按组别过滤
<li>抽验捋肩带添加疵点界面不用跳出选择框
<li>删除疵点不需要点入疵点编辑界面
<li>员工姓名显示错误解决
<li>一检、二检查看汇总和审批界面改为表格
<li>个人信息界面的数据统计改为表格显示
<li>查看汇总和报表审批界面增加返修活检验流程
<li>增加数据表sklcc_return_check
<li>权限管理界面取消配置批号过滤时间的功能
<li>抽验界面通过不通过的显示调整
</ul></td>
<td><ul>
<li>views.py
<li>forms.py
<li>urls.html
<li>management.html
<li>function.js
<li>table_haven_submitted.html
<li>table_stage_repair.html
<li>function_management.js
<li>增添daily_return_check.html
<li>recheck.js
<li>recheck.html
</ul></td>

<tr>
<td>2014-07-18</td>
<td><ul>
<li>二检捋肩带可增加疵点信息，更新了sklcc_recheck_bald表的设计</li>
<li>抽验界面的一检检验员显示的BUG修复（原本显示二检）</li>
<li>个人漏验历史记录查询明细</li>
<li>Excel导出修正</li>
<li>一检修复查看明细表出现的一道工序多个员工负责，最终只显示一个员工的显示BUG</li>
<li>二检批次号过多，权限管理界面增加批次号过滤的时间控制</li>
<li>二检捋肩带的员工列表过滤为所有一检员工</li>
<li>将抽验结论添加到抽验录入界面</li>
<li>权限管理界面添加筛选功能</li>
<li>二检修改批次显示顺序的BUG修复</li>
</ul></td>
<td><ul>
<li>views.py
<li>forms.py
<li>urls.html
<li>management.html
<li>function.js
<li>table_haven_submitted.html
<li>table_stage_repair.html
<li>function_management.js
<li>recheck.js
<li>recheck.html
</ul></td>

<tr>
<td>2014-07-14</td>
<td><ul>
<li>修正了网站后台BUG</li>
<li>完善个人信息页面，增加历史记录查询,修改二检组别顺序的实现</li>
<li>捋肩带往数据库写入功能的实现</li>
<li>后台处理了数据库中存在只有工序序号没有工序名称的情况</li>
<li>抽验提交没有疵点的情况处理</li>
<li>数据库中不再存入和用户名username绑定的数据信息，转为和员工姓名绑定</li>
<li>阶段返修记录表查询的实现</li>
<li>捋肩带记录表查询的实现</li>
<li>添加权限：阶段返修记录表，捋肩带记录表</li>
<li>权限修改的界面，权限管理和部分报表折线图由部门选择改为拥有权限</li>
</ul></td>
<td><ul>
<li>创建新表sklcc _ recheck _ bald</li>
<li>funtion_recheck.js
<li>recheck.html
<li>management.html
<li>personal.html
<li>table_stage_repair.html
<li>table_bald_history.html
<li>table_haven_submitted.html
<li>views.py
<li>forms.py
<li>urls.py

</ul></td>

<tr>
<td>2014-07-11</td>
<td><ul>
<li>登陆改为登录</li>
<li>增加员工的页面可以不填从...复制权限</li>
<li>重新扫描已扫描的条码时，unknown显示为未知</li>
<li>历史记录表查询的实现</li>
<li>无疵点记录更新到数据库的实现</li>
<li>更新了sklcc _ info数据表的设计，部分字段可为空</li>
<li>条码扫描没有疵点直接提交不再要求确认</li>
<li>疵点数量直接用小键盘输入</li>
<li>扫描条码可用小键盘输入</li>
<li>疵点按疵点编号排序</li>
<li>工序添加“裁剪”、“整烫”，责任人是“整烫组”</li>
<li>用户信息实现，可查看当天返修率、漏验率、修改密码、修改显示效果等等</li>
<li>二检查看汇总和报表审批的检验样本数量BUG修复</li>
<li>二检增加清款批次的选择框，实现了增加一检清款批次功能</li>
<li>捋肩带界面实现</li>
</ul></td>
<td><ul>
<li>LogIn.html</li>
<li>manage_function.html</li>
<li>dataentry js.js</li>
<li>views.py</li>
<li>增添form.py</li>
<li>models.py</li>
<li>数据表sklcc_info的设计</li>
<li>table_haven_submitted.html</li>
<li>dataentry.html</li>
<li>recheck.html</li>
<li>recheck.js</li>
<li>...涉及文件数较多，采用直接覆盖的方式更新</li>
</ul></td>


<tr>
<td>2014-06-17</td>
<td><ul>
<li>记住我功能完善（对勾的勾选）</li>
<li>权限管理的复制权限的功能实现</li>
<li>权限管理的部门管理将部门编号排序显示，用户管理标签页按员工号排序显示</li>
<li>权限分配部门时，增添全选按钮</li>
<li>一个工号可以有多个账号，但是一个工号只对应一个员工姓名，账号不可重复</li>
<li>实现了用户名修改之后各个表格数据库同步的功能</li>
<li>重新修正了一检查看汇总的权限控制</li>
<li>重新修正了二检查看汇总和二检审批的权限控制</li>
<li>所有表格的大标题区分出一检和二检</li>
<li>折线图实现了输入框动态刷新功能</li>
<li>权限管理界面权限的按钮修改成了标签</li>
<li>权限管理界面部门管理标签页的滚动条的实现</li>
<li>二检审批和查看汇总界面的修改</li>
</ul></td>
<td>
<ul>
<li>views.py</li>
<li>LogIn.html</li>
<li>management.html</li>
<li>tables.html</li>
<li>table_read_only.html</li>
<li>tables_check.html</li>
<li>tables_recheck.html</li>
<li>tables_recheck_check.html</li>
<li>tables_recheck_read_only.html</li>
<li>line_chart.html</li>
<li>line_chart.js</li>
<li>manage_function.js</li>
<li>增添bootstrap-combobox.js</li>
<li>choose_recheck.html</li>
<li>choose_recheck_check.html</li>
</ul>
</td>
</tr>


<tr>
<td>2014-06-07</td>
<td>
<ul>
<li>记住我功能实现</li>
<li>批量提交功能的实现</li>
</td>
<td>
<ul>
<li>增添jquery.cookie.js</li>
<li>LogIn.html</li>
<li>choose.html</li>
<li>choose_check.html</li>
</ul>
</td>
</tr>

<tr>
<td>2014-06-06</br><h2>v0.1</h2></td>
<td> 
<ul>
<li>登录界面：员工号->账号</li>
<li>权限管理界面:用户权限修改功能的修复</li>
<li>权限管理界面HTML模板Bug修复</li>
<li>适应分辨率的界面微调：两个查看汇总，两个审批</li>
<li>未知工序功能的实现，写入数据库为unknown，前端显示为未知</li>
<li>时间显示，去掉年份和秒数</li>
<li>由于测试账号的所有信息（账号，工号和密码）一致，修改账号信息为不一致之DEBUG修复</li>
<li>二检无法录入的bug修复</li>
<li>权限管理：部门管理界面下拉条添加</li>
<li>员工查看汇总没有权限的BUG修复,二检权限判定的修复</li>
</ul>
</td>
<td>
<ul>
<li>login.html</li>
<li>views.py</li>
<li>management.html</li>
<li>dataentry.html</li>
<li>choose.html</li>
<li>choose_check.html</li>
<li>recheck.html</li>
<li>choose_recheck.html</li>
<li>choose_check_recheck.html</li>
<li>funtion.js</li>
<li>function_check.js</li>
<li>function_read_only.js</li>
<li>function_recheck.js</li>
<li>function_recheck_check.js</li>
<li>function_recheck_read_only.js</li>
<li>recheck.js</li>
<li>base.html</li>
</ul>
</td>
</tr>



</table>