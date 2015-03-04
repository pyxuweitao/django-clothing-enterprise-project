﻿# 2014-09-02 written by XuWeitao

# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.template.loader import get_template
from django.db import connection, connections, transaction
from django.views.decorators.cache import cache_control
from xml.etree import ElementTree
import re
import datetime
import time
import sys
import os
from django.utils import simplejson
from EQ_IM_TIME import *
import uuid
import urllib
import urllib2
import copy
from utilitys import *
from measure import *
import logging


def initLogging( logFilename ):
	"""Init for logging"""
	logging.basicConfig( level = logging.DEBUG, format = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
	                     datefmt = '%m-%d %H:%M', filename = logFilename, filemode = 'w' )
	# define a Handler which writes INFO messages or higher to the sys.stderr


	console = logging.StreamHandler( )
	console.setLevel( logging.INFO )
# set a format which is simpler for console use
	formatter = logging.Formatter( 'LINE %(lineno)-4d : %(levelname)-8s %(message)s' )
# tell the handler to use this format
	console.setFormatter( formatter )
	logging.getLogger( '' ).addHandler( console )

initLogging( "E:\\debug.log" )

DEPT_SHOP1 = ['201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211', '212']
DEPT_SHOP2 = ['213', '214', '215', '216', '217', '218', '219', '220', '221', '222', '223', '224']
DEPT_SHOP3 = ['225', '226', '227', '228', '229', '230']


class History:
	batch = ""
	createtime = ""
	passtime = ""
	returnno = 0
	departmentno = ""
	inspector_no = ""
	inspector = ""
	serialno = ""


class temp_Info:
	inspector = ""
	inspector_no = ""
	state = 0
	questionname = ""
	questionno = 0
	workname = ""
	workno = 0
	employee = ""
	employeeno = ""
	type_data = 0
	returnno = 0
	barcode = ""
	boxno = 0
	number_pack = 0
	serialno = ""
	batch = ""
	departmentno = ""
	check_id = ""
	check_type = ""


class Check_type:
	def __init__( self ):
		self.check_id = ""
		self.check_type = ""


class temp_info:
	barcode = ""
	serialno = ""
	batch = ""


class type_count_three:
	weak = 0
	bad = 0
	strong = 0


class Record_info:
	serialno = ''
	createtime = ''
	inspector = ''
	inspector_no = ''
	state = 2
	assessor = ''
	assessor_no = ''
	assesstime = ''
	batch = ''
	departmentno = ''
	totalnumber = 0
	totalreturn = 0
	#add 3 elements
	weak = 0
	bad = 0
	strong = 0
	url = ""
	check_id = ""
	check_type = ""
	batchnumber = 0


class Record_number_off:
	def __init__( self ):
		state = 0
		createtime = ""
		batch = ""
		check_id = 0
		check_type = ""
		totalnumber = 0


class Department_info:
	departmentname = ""
	departmentno = ""
	ischosen = 0


class Question:
	def __init__( self ):
		self.questionno = 0
		self.questionname = ""
		self.questiontype = 0
		self.ischosen = 0


class Authority:
	no = 0
	name = ""
	url = ""


class Em_authority:
	employeeno = ""
	employee = ""
	button_list = []


class Button:
	departmentno = ""
	department = ""
	id = 0
	name = ""


class Myinfo:
	def __init__( self, employeeno, date ):
		self.employeeno = employeeno
		self.date = date
		self.check_totalnumber = get_check_totalnumber( employeeno, date )
		self.check_totalreturn = get_check_totalreturn( employeeno, date )
		self.question_list = get_personal_miss_history( employeeno, date )
		if self.check_totalnumber == 0:
			self.check_percentage = '0%'
		else:
			self.check_percentage = str(
				format( float( self.check_totalreturn ) / float( self.check_totalnumber ), '.2%' ) )

		self.check_miss = get_check_miss( employeeno, date )
		self.recheck_totalnumber = get_recheck_totalnumber( employeeno, date )  #sampletotalnumber
		self.recheck_totalreturn = get_recheck_totalreturn( employeeno, date )

		if self.recheck_totalnumber == 0:
			self.recheck_percentage = '0%'
		else:
			self.recheck_percentage = str(
				format( float( self.recheck_totalreturn ) / float( self.recheck_totalnumber ), '.2%' ) )
		self.bald_totalnumber = get_today_bald( employeeno, date )


class Bald_info:
	def __init__( self ):
		self.createtime = ""
		self.totalnumber = 0
		self.recheckor = ""
		self.recheckor_no = ""
		self.info = { }


class Return_check_info:
	def __init__( self ):
		self.serialno = ""
		self.type = 1
		self.createtime = ""
		self.ok = 0
		self.batch = ""
		self.totalnumber = 0
		self.totalreturn = 0
		self.realreturn = 0
		self.state = 0
		self.question_list = []
		self.employeeno = ""
		self.employee = ""


class Rule:
	def __init__( self ):
		self.employeeno = ''
		self.employee = ''
		self.typename = ''
		self.typeno = 0


class Workno_return:
	def __init__( self ):
		self.workname = ''
		self.returnno = 0


class History_form:
	category = "/"
	serialno = "/"
	createtime = "/"
	# pre_submit
	inspector = "/"
	inspector_no = "/"
	# pre_check and sec_check
	assessor = "/"
	assessor_no = "/"
	assesstime = "/"
	# sec_submit
	recheckor = "/"
	recheckor_no = "/"
	totalnumber = "/"
	totalreturn = "/"
	deaprtmentno = "/"
	deaprtment = "/"
	batch = "/"
	url = "/"


def get_all_department( ):
	Raw = Raw_sql( )
	department_list = list( )
	Raw.sql = "select departmentno, department from sklcc_department order by departmentno"
	department_list_found = Raw.query_all( )
	if department_list_found != False:
		for department in department_list_found:
			department_info = Department_info( )
			department_info.departmentname = department[1]
			department_info.departmentno = department[0]
			department_list.append( department_info )
	return department_list


def written_into_sklcc_effciency( ):
	Raw = Raw_sql( )
	Raw.sql = "select Top 1 form7_real_work_time from sklcc_config"
	target = Raw.query_one( )
	real_work_time = target[0] if target != False and target != None else 0
	T = Current_time( )
	date = T.set_date_yesterday( ).split( " " )[0]
	Raw.sql = "select distinct username from sklcc_employee_authority where authorityid = 1 and username not in " \
	          "( select distinct username from sklcc_employee_authority where authorityid = 7 )"
	target_list = Raw.query_all( )
	recheckor_list = []
	if target_list != False:
		for target in target_list:
			employeeno = find_employeeno( target[0] )
			recheckor_list.append( { 'employeeno': employeeno, 'employee': find_em_name( employeeno ) } )

	Raw.sql = '''select recheckor_no, recheckor, sum( total * slowtime )  from
				( select recheckor, recheckor_no, batch, sum( samplenumber ) total from sklcc_recheck_info a join sklcc_recheck_content b
					on  a.serialno = b.serialno  where left( a.createtime, 10 ) = '%s' group by batch, recheckor, recheckor_no ) recheck,
				( select batch, slowtime from [BDDMS_MSZ].[dbo].ProduceMaster, [BDDMS_MSZ].[dbo].ProduceStyle
					where [BDDMS_MSZ].[dbo].ProduceStyle.producemasterid = [BDDMS_MSZ].[dbo].ProduceMaster.producemasterid and workname = ''' % date + "'检验'".decode(
		'utf-8' ) + ''') produce where produce.batch = recheck.batch group by recheckor_no, recheckor'''
	res_list = Raw.query_all( )
	if res_list != False:
		for res in res_list:
			recheckor_no = res[0]
			recheckor = res[1]
			work_time = res[2]
			Raw.sql = "insert into sklcc_effciency( employeeno, employee, date, work_time, real_work_time, effciency )" \
			          "values( '%s', '%s', '%s', %f, %f, %f )" % (
			          recheckor_no, recheckor, date, work_time, real_work_time,
			          round( float( work_time ) / float( real_work_time ) if real_work_time != 0 else 0, 4 )  )
			Raw.update( )

	if res_list != False:
		for one in recheckor_list:
			if one['employeeno'] not in [rec[0] for rec in res_list]:
				recheckor_no = one['employeeno']
				recheckor = one['employee']
				work_time = 0.0
				Raw.sql = "insert into sklcc_effciency( employeeno, employee, date, work_time, real_work_time, effciency )" \
				          "values( '%s', '%s', '%s', %f, %f, %f )" % (
				          recheckor_no, recheckor, date, work_time, real_work_time, 0 )
				Raw.update( )
	else:
		for one in recheckor_list:
			recheckor_no = one['employeeno']
			recheckor = one['employee']
			work_time = 0.0
			Raw.sql = "insert into sklcc_effciency( employeeno, employee, date, work_time, real_work_time, effciency )" \
			          "values( '%s', '%s', '%s', %f, %f, %f )" % (
			          recheckor_no, recheckor, date, work_time, real_work_time, 0 )
			Raw.update( )
	return 'ok'


def sysmessage( msg, receiver ):
	try:
		im = { }
		receiveaccount = { }
		im['msg'] = msg
		receiveaccount['receiver'] = receiver
		url_value0 = urllib.urlencode( im )
		url_value1 = urllib.urlencode( receiveaccount )
		address = os.getcwd( ) + '\\RTX_config.txt'
		fp = open( address, 'r+' )
		RTX_URL = fp.readline( ).strip( '\n' )
		fp.close( )
		url = r'http://' + RTX_URL + r'/sendnotify.cgi'
		full_url = url + '?' + url_value0 + '&' + url_value1
		req = urllib2.Request( full_url )
		response = urllib2.urlopen( req )
	except Exception, e:
		make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )


def get_all_RTX_receivers( ):
	try:
		fp = open( os.getcwd( ) + '\\RTX_config.txt', 'r+' )
		receivers = []
		one = fp.readline( )
		one = fp.readline( )
		while len( one ) != 0:
			receivers.append( one.strip( '\n' ) )
			one = fp.readline( )
		fp.close( )
		return receivers
	except Exception, e:
		make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )


class timer( threading.Thread ):
	def __init__( self ):
		threading.Thread.__init__( self )
		self.thread_stop = False
		self.timepoint_for_EQ = []
		self.timepoint_for_EQ.append( '10:00' )
		self.timepoint_for_EQ.append( '12:00' )
		self.timepoint_for_EQ.append( '15:00' )
		self.timepoint_for_EQ.append( '18:00' )
		self.timepoint_for_RTX = []
		self.timepoint_for_RTX.append( '12:00' )
		self.timepoint_for_RTX.append( '17:00' )
		self.timepoint_for_check_measure = []
		self.timepoint_for_check_measure.append( '16:00' )

	def run( self ):
		department_list = get_all_department( )
		while True:
			Raw = Raw_sql( )
			timenow = time.strftime( '%H:%M', time.localtime( time.time( ) ) )
			print timenow
			if timenow in self.timepoint_for_EQ:
				try:
					for department in department_list:
						departmentno = department.departmentno
						content = get_three_workno_to_EQ( time.strftime( '%Y-%m-%d', time.localtime( time.time( ) ) ),
						                                  departmentno )
						timesend( departmentno, '300', content, '1', '0' )
				except Exception, e:
					make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) + '(EQ)' )
			if timenow == '14:28':
				try:
					written_into_sklcc_effciency( )
				except Exception, e:
					make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) + 'written_into_effciency' )
			if timenow in self.timepoint_for_RTX:
				try:
					timemes = u'中午好' if timenow == self.timepoint_for_RTX[0] else u'下午好'
					receives = get_all_RTX_receivers( )
					for receiver in receives:
						msg = u'尊敬的用户，' + timemes + u',请您及时登录质检系统查看报表审批情况，谢谢。'
						sysmessage( msg.encode( 'gb2312' ), receiver )
				except Exception, e:
					make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) + 'RTX' )
			time.sleep( 60 )

	def stop( self ):
		self.thread_stop = True


t = timer( )
t.start( )
send_to_screen( ).start( )


def get_personal_miss_history( employeeno, date ):
	try:
		Raw = Raw_sql( )
		Raw.sql = "select serialno from sklcc_recheck_info where inspector_no = '%s' and left( createtime, 10 ) = '%s'" % (
		employeeno, date )
		target_list = Raw.query_all( )
		returnlist = []
		if target_list != False:
			for target in target_list:
				serialno = target[0]
				Raw.sql = "select sum( returnno ), questionno, questionname from sklcc_recheck_content where serialno = '%s' group by questionno, questionname " % serialno
				question_list = Raw.query_all( )
				for question in question_list:
					if question[1] == 0:
						continue
					returnno = question[0]
					questionno = question[1]
					questionname = question[2]
					temp = str( returnno ) + "X" + str( questionname.encode( 'utf-8' ) )
					returnlist.append( temp )
		return returnlist
	except Exception, e:
		make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )


def get_all_question( ):
	Raw = Raw_sql( )
	Raw.sql = 'select questioncode, questionno from QCQuestion WITH (NOLOCK) order by questionno'
	target_list = Raw.query_all( 'MSZ' )

	question_list = []
	for target in target_list:
		question = Question( )
		question.questionname = target[0].decode( 'gbk' )
		question.questionno = target[1]
		question.questiontype = get_question_type( target[1] )
		question_list.append( question )
	return question_list


def warning( request ):
	html = get_template( 'no_permisson.html' )
	return TemplateResponse( request, html )


def base( request ):
	Raw = Raw_sql( )
	username = request.session['username']
	url_list = []
	Raw.sql = "select distinct url from sklcc_authority a join sklcc_employee_authority b on a.authorityid = b.authorityid " \
	          "where username = '%s'" % username
	target_list = Raw.query_all( )

	if target_list != False:
		for one in target_list:
			url_list.append( one[0] )
	return HttpResponse( simplejson.dumps( url_list, ensure_ascii = False ) )


def find_username( employeeno ):
	Raw = Raw_sql( )
	Raw.sql = "select username from sklcc_employee where employeeno = '%s'" % employeeno
	target = Raw.query_one( )
	return target[0]


def find_employee_in_Employee( employeeno ):
	Raw = Raw_sql( )
	Raw.sql = "select employee from Employee WITH (NOLOCK) where employeeno = '%s'" % employeeno
	target = Raw.query_all( 'MSZ' )
	if target != False or len( target ) == 1:
		return target[0][0]
	else:
		return False


def find_questionname( questionno ):
	Raw = Raw_sql( )
	Raw.sql = "select QuestionCode from QCQuestion WITH (NOLOCK) where QuestionNO = %d" % questionno
	target = Raw.query_one( 'MSZ' )
	return target[0]


def find_workname_in_sklcc_recheck_content( serialno, workno ):
	Raw = Raw_sql( )
	Raw.sql = "select workname from sklcc_recheck_content where serialno = '%s' and workno = %d" % ( serialno, workno )
	target = Raw.query_all( )
	return target[0][0]


def find_status_list( username ):
	Raw = Raw_sql( )
	Raw.sql = "select distinct authorityid from sklcc_employee_authority where username = '%s'" % username
	target_list = Raw.query_all( )
	status = list( )

	if target_list != False:
		for target in target_list:
			status.append( target[0] )
	return status


def find_pre_table( employeeno, authorityid, start, end ):
	Raw = Raw_sql( )
	pre_tables = []
	if authorityid == 2:
		Raw.sql = "select serialno, createtime, inspector, inspector_no, assessor, assessor_no, assesstime, totalnumber, totalreturn," \
		          " batch, departmentno from sklcc_record where inspector_no = '%s' and state = 1 and left(assesstime,10) >= '%s' and left(assesstime,10) <= '%s'" % (
		          employeeno, start, end )
	elif authorityid == 4:
		Raw.sql = "select serialno, createtime, inspector, inspector_no, assessor, assessor_no, assesstime, totalnumber, totalreturn," \
		          " batch, departmentno from sklcc_record where assessor_no = '%s' and state = 1 and left(assesstime,10) >= '%s' and left(assesstime,10) <= '%s'" % (
		          employeeno, start, end )
	target_list = Raw.query_all( )

	if target_list != False:
		for target in target_list:
			form = History_form( )
			form.category = "一检"
			form.serialno = target[0]
			form.createtime = target[1][:-10]
			form.inspector = target[2]
			form.inspector_no = target[3]
			form.assessor = target[4]
			form.assessor_no = target[5]
			form.assesstime = target[6][:-10]
			form.totalnumber = str( target[7] )
			form.totalreturn = str( target[8] )
			form.batch = target[9]
			form.departmentno = target[10]
			form.deaprtment = find_department_name( form.departmentno )
			form.url = "/read_only_table?history#%s/" % ( form.serialno )
			pre_tables.append( form )
	return pre_tables


def find_sec_table( employeeno, authorityid, start, end ):
	Raw = Raw_sql( )
	sec_tables = []
	if authorityid == 3:
		Raw.sql = "select serialno, createtime, inspector, inspector_no, recheckor, recheckor_no, assesstime," \
		          " batch, departmentno, department, leader, leader_no from sklcc_recheck_info where recheckor_no = '%s' and state = 1 and left(assesstime,10) >= '%s' and left(assesstime,10) <= '%s'" % (
		          employeeno, start, end )
	elif authorityid == 5:
		Raw.sql = "select serialno, createtime, inspector, inspector_no, recheckor, recheckor_no, assesstime," \
		          " batch, departmentno, department, leader, leader_no from sklcc_recheck_info where leader_no = '%s' and state = 1 and left(assesstime,10) >= '%s' and left(assesstime,10) <= '%s'" % (
		          employeeno, start, end )
	target_list = Raw.query_all( )

	if target_list != False:
		for target in target_list:
			form = History_form( )
			form.category = "二检"
			form.serialno = target[0]
			form.createtime = target[1][:-10]
			form.inspector = target[2]
			form.inspector_no = target[3]
			form.recheckor = target[4]
			form.recheckor_no = target[5]
			form.assesstime = target[6][:-10]
			form.batch = target[7]
			form.departmentno = target[8]
			form.deaprtment = target[9]
			form.assessor = target[10]
			form.assessor_no = target[11]
			Raw.sql = "select samplenumber, returnno, questionno from sklcc_recheck_content where serialno = '%s'" % form.serialno
			is_serialno_list = Raw.query_all( )
			totalnumber = 0
			totalreturn = 0
			for one in is_serialno_list:
				totalnumber += one[0]
				totalreturn += one[1]

			form.totalnumber = str( totalnumber )
			form.totalreturn = str( totalreturn )
			form.url = "/recheck_read_only_table?history#%s" % ( form.serialno )
			sec_tables.append( form )
	return sec_tables


def change_distance_date_to_str_have_year( distance ):
	distance_new = []
	for one in distance:
		distance_new.append( str( one )[0:10] )
	return distance_new


def change_distance_date_to_str_not_have_year( distance ):
	distance_new = []
	for one in distance:
		distance_new.append( str( one )[5:10] )
	return distance_new


def get_three_workno_to_EQ( date, departmentno ):
	Raw = Raw_sql( )
	reload( sys )
	sys.setdefaultencoding( 'utf-8' )
	Raw.sql = """select TOP 3 sum( returnno ), workname from sklcc_table
				where serialno in
				( select serialno from sklcc_record where departmentno = '%s' and left( createtime, 10 ) = '%s' )
				group by workname
				order by sum( returnno ) desc""" % ( departmentno, date )
	target_list = Raw.query_all( )

	three_workno = []
	if target_list != False:
		for target in target_list:
			t = Workno_return( )
			t.returnno = target[0]
			t.workname = target[1]
			three_workno.append( t )

	res = "当前出现疵点最高的工序:@@"
	res += str( departmentno )
	if len( three_workno ) == 0:
		res += "@当前无统计数据@@"
	else:

		for one in three_workno:
			res += one.workname
			res += ':'
			res += str( one.returnno )
			res += '件@'
		res += '@' * ( 3 - len( three_workno ) )
	T = Current_time( )
	res += "@当前统计数据截止到%s#1" % T.get_time( )[0:8]
	return res.decode( 'utf-8' )


def time_form( string ):
	year = int( string.split( '-' )[0] )
	month = int( string.split( '-' )[1] )
	day = int( string.split( '-' )[2] )
	time = datetime.datetime( year, month, day )
	return time


def get_time_distance_list( start, end ):
	distance = list( )
	start = time_form( start )
	end = time_form( end )
	distance.append( start.date( ) )
	for i in range( (end - start).days ):
		start = start + datetime.timedelta( days = 1 )
		distance.append( start.date( ) )
	#distance.append( end.date() )
	return distance


def fail( request, url ):
	html = ''
	if url == '404':
		html = get_template( 'error_hint_404.html' )
	elif url == '500':
		html = get_template( 'error_hint_500.html' )
	return TemplateResponse( request, html )


def login( request ):
	html = get_template( 'LogIn.html' )
	return TemplateResponse( request, html, locals( ) )


#1 the em_number or password -> null
#2 the em_number or password -> wrong
def submit_id( request ):
	username = request.GET['username'].upper( )
	em_password = request.GET['em_password'] if 'em_password' in request.GET else True

	Raw = Raw_sql( )
	Raw.sql = "select username from sklcc_employee_authority where authorityid = 7"
	superuser = [one[0].upper( ) for one in Raw.query_all( )]
	if not username and not em_password:
		return HttpResponseRedirect( '/login/#1' )
	else:
		Raw.sql = "select password, employeeno, employee from sklcc_employee where username = '%s'" % username
		target = Raw.query_one( )
		if em_password == True and username not in superuser and target:
			request.session['username'] = username
			request.session['em_password'] = em_password
			request.session['employee'] = target[2]
			request.session['employeeno'] = target[1]
			status = find_status_list( username )
			request.session['status'] = status
			return HttpResponse( )
		if target and target[0] == em_password:
			request.session['username'] = username
			request.session['em_password'] = em_password
			request.session['employee'] = target[2]
			request.session['employeeno'] = target[1]
			status = find_status_list( username )
			request.session['status'] = status
			if 7 in status:
				return HttpResponseRedirect( '/admini/' )
			elif 4 in status:
				return HttpResponseRedirect( '/choose_check/' )
			elif 5 in status:
				return HttpResponseRedirect( '/choose_check_recheck/' )
			elif 0 in status:
				return HttpResponseRedirect( '/url_dataentry/' )
			elif 1 in status:
				return HttpResponseRedirect( '/recheck/' )
			elif 2 in status:
				return HttpResponseRedirect( '/choose/' )
			elif 3 in status:
				return HttpResponseRedirect( '/choose_recheck/' )
			elif 6 in status:
				return HttpResponseRedirect( '/line_chart/' )
			elif 8 in status:
				return HttpResponseRedirect( '/form4/' )
			elif 9 in status:
				return HttpResponseRedirect( '/form5/' )
			elif 10 in status:
				return HttpResponseRedirect( '/form1/' )
			elif 11 in status:
				return HttpResponseRedirect( '/form2/' )
			elif 12 in status:
				return HttpResponseRedirect( '/form3/' )
			elif 13 in status:
				return HttpResponseRedirect( '/form6/' )
			elif 14 in status:
				return HttpResponseRedirect( '/form7/' )
			elif 15 in status:
				return HttpResponseRedirect( '/form0/' )
			elif 16 in status:
				return HttpResponseRedirect( '/form8/' )
			elif 17 in status:
				return HttpResponseRedirect( '/form9/' )
			elif 18 in status:
				return HttpResponseRedirect( '/bar_question_chart/' )
			elif 19 in status:
				return HttpResponseRedirect( '/pie_chart/' )
			elif 21 in status:
				return HttpResponseRedirect( '/bar_measure_chart/' )
			elif 22 in status:
				return HttpResponseRedirect( '/style_measure/' )
			else:
				return HttpResponseRedirect( '/login/#3' )
		else:
			return HttpResponseRedirect( '/login/#2' )


def logout( request ):
	del request.session['employeeno']
	del request.session['em_password']
	del request.session['username']
	del request.session['status']
	if 'no_redirect' in request.GET:
		return HttpResponse( 'ok' )
	return HttpResponseRedirect( '/login/' )


################################################*** first check ***#####################################################
##################################### *@*       start of dataentry        *@* ##########################################
def url_dataentry( request ):
	Raw = Raw_sql( )
	Raw.sql = "select top 1 login_switch from sklcc_config"
	login_switch = Raw.query_one( )[0]
	status = request.session['status']
	if 0 in status:
		html = get_template( 'dataentry.html' )
		username = request.session['username']
		employeename = request.session['employee']
		em_number = request.session['employeeno']
		return TemplateResponse( request, html, locals( ) )
	else:
		return HttpResponseRedirect( '/warning/' )


def get_info( barcode_num, inspector_no ):
	Raw = Raw_sql( )
	T = Current_time( )
	today = T.get_date( )

	Raw.sql = "SELECT TOP 1 b.inspector_no, b.state FROM [SKLCC].DBO.sklcc_info a JOIN [SKLCC].DBO.sklcc_record b" \
	          " WITH(NOLOCK) ON a.serialno = b.serialno WHERE barcode = '%s'" % barcode_num
	target = Raw.query_one( )

	if target != False:
		if target[0] != inspector_no:
			return dict( state = 6 )
		else:
			if target[1] == 2:
				state = 2
			else:
				state = 3
	else:
		state = 1


	barcode = int( barcode_num[0:5] )
	packno  = int( barcode_num[6:10] )
	Raw.sql = """SELECT TOP 1 a.Batch, a.DepartmentNo, a.number, a.styleno, b.packid, b.size, b.number, a.producemasterid
	 FROM ProduceMaster a JOIN producepack b WITH (NOLOCK) ON a.producemasterid = b.producemasterid
	  WHERE Barcode = SUBSTRING('%s',1,5) AND FormState = '审核' AND packno = SUBSTRING( '%s', 6, 5 )"""%( barcode_num, barcode_num )
	target_mas = Raw.query_one( 'MSZ' )
	#if cannot find this barcode, return state = 0 | can find, return state = 1 | can find in info table and can be edited, state = 2 | can find in info table but cannot be edited, state = 3
	if not target_mas:
		#info = dict( state = 0, measured = measured )
		info = dict( state = 0 )
		return info

	#get masterid
	masterid     = target_mas[7]
	batch        = target_mas[0].decode( 'gbk' )
	departmentno = target_mas[1]
	total_number = target_mas[2]
	styleno      = target_mas[3]
	packid       = target_mas[4]
	size         = target_mas[5]
	number_pack  = target_mas[6]


	info = dict( state = state, styleno = styleno, barcode = barcode, packno = packno,
	             masterid = masterid, total_number = total_number, packid = packid, size = size,
	             number_pack = number_pack, departmentno = departmentno, batch = batch )
	return info


def get_all_check_type( ):
	Raw = Raw_sql( )
	Raw.sql = "select check_id, check_type from sklcc_check_type where check_id != '2'"
	check_type_list = []
	target_list = Raw.query_all( )
	if target_list != False:
		for target in target_list:
			t = Check_type( )
			t.check_id = target[0]
			t.check_type = target[1]
			check_type_list.append( t )
	return check_type_list


def number_off( request ):
	if 0 not in request.session['status']:
		return HttpResponseRedirect( '/warning/' )
	Raw = Raw_sql( )
	Raw.sql = "select top 1 login_switch from sklcc_config"
	login_switch = Raw.query_one( )[0]
	em_number = request.session['employeeno']
	employeename = request.session['employee']
	html = get_template( 'number_off.html' )
	question_list = get_all_question( )
	question_weak = []
	question_bad = []
	question_strong = []
	for one in question_list:
		if one.questiontype == 0:
			question_weak.append( one )
		elif one.questiontype == 1:
			question_bad.append( one )
		elif one.questiontype == 2:
			question_strong.append( one )
	department_list = get_all_department( )
	check_type_list = get_all_check_type( )
	for check_type in check_type_list:
		if check_type.check_id == '1':
			check_type_list.remove( check_type )
	return TemplateResponse( request, html, locals( ) )


def get_measure_info_by_barcode( barcode, inspector_no ):
	Raw = Raw_sql( )
	Raw.sql = "select partition, measure_type, measure_res, symmetry1, symmetry2, count_id, a.serialno from sklcc_measure_info a" \
	          " join sklcc_measure_record b on a.serialno = b.serialno where barcode" \
	          " = '%s' and inspector_no = '%s' order by count_id" % ( barcode, inspector_no )
	target_list = Raw.query_all( )
	if target_list != False:
		serialno = target_list[0][6]
		res = { }
		for target in target_list:
			if target[0] not in res.iterkeys( ):
				res[target[0]] = []
			res[target[0]].append( [target[3], target[4]] ) if target[1] == 1 else res[target[0]].append( [target[2]] )

		res['serialno'] = serialno
		res['barcode'] = barcode
		return res
	else:
		return False


def get_partition_table( request = None, styleno = '', size = '', control = True ):
	Raw = Raw_sql( )
	xml = ""
	if request != None:
		styleno = request.GET['styleno']
		size = request.GET['size']
		control = False
	Raw.sql = "select distinct size from sklcc_style_measure where styleno = '%s'" % styleno
	target_list = Raw.query_all( )
	if target_list != False:
		if size in [target[0] for target in target_list]:
			Raw.sql = "select partition, common_difference, symmetry, measure_res from sklcc_style_measure where measure_or_not" \
			          " = 1 and size = '%s' and styleno = '%s'" % ( size, styleno)
			partition_list = Raw.query_all( )

			if partition_list != False:
				xml += """<ME>"""
				for partition in partition_list:
					xml += """<measure partition = "%s" common_difference = "%.2f" symmetry = "%.2f" measure_res = "%.2f"/>""" % (
					partition[0], partition[1], partition[2], partition[3] )
				xml += """</ME>"""
	return xml if control else HttpResponse( '<xml>' + xml + '</xml>' )


def update_info( request ):
	try:
		reload(sys)
		sys.setdefaultencoding('utf-8')
		Raw = Raw_sql( )
		T = Current_time( )
		inspector_no = request.session['employeeno']
		barcode = request.GET['code']
		info_ini = get_info( barcode, inspector_no )
		xml = """"""
		if info_ini['state'] == 0:
			xml += """<state value = "0"></state></info></xml>"""
			return HttpResponse( xml )

		if info_ini['state'] == 4:
			xml += """<state value = "4"></state></info></xml>"""
			return HttpResponse( xml )

		if info_ini == False:
			return HttpResponse( """<xml><info><state value = "5"></state></info></xml>""" )

		if info_ini['state'] == 6:
			return HttpResponse( """<xml><info><state value = "6"></state></info></xml>""" )

		# Raw.sql = "select serialno, measure_count from sklcc_measure_record where inspector_no = '%s' and left( createtime, 10 ) = '%s' and " \
		#           "batch = '%s' and size = '%s'" % ( inspector_no, today, info_ini['batch'], info_ini['size'] )
		# target = Raw.query_one( )
		#
		# if target == False:
		# 	serialno = uuid.uuid1( )
		# 	createtime = T.time_str
		# 	written_into_measure_record(
		# 		dict( serialno = serialno, createtime = createtime, inspector_no = inspector_no, inspector = inspector,
		# 		      batch = info_ini['batch'], styleno = info_ini['styleno'], size = info_ini['size'],
		# 		      measure_count = 0 ) )
		#get_info return False refers to not finish measuring task today

		xml += """<xml>"""
		xml += """<info>"""
		#cannot find this barcode in producemaster

		#can find in info table and can be edited
		if info_ini['state'] == 2:
			xml += """<state value = "2"></state>"""
		#can find in producemaster but cannot find in info table
		elif info_ini['state'] == 1:
			xml += """<state value = "1"></state>"""
		else:
			xml += """<state value = "3"></state>"""

		xml += """<scan_id>%s</scan_id>""" % info_ini['batch']
		xml += """<scan_count>%s</scan_count>""" % info_ini['number_pack']
		xml += """<scan_group>%s</scan_group>""" % info_ini['departmentno']
		xml += """<scan_model>%s</scan_model>""" % info_ini['size']
		xml += """<scan_total_number>%s</scan_total_number>""" % info_ini['total_number']
		xml += """<scan_package_id>%s</scan_package_id>""" % info_ini['packno']
		xml += """<scan_measure_count>0</scan_measure_count>"""
		xml += """</info>"""



		###find question
		Raw.sql = "select QuestionCode, isStrong, isBad, QuestionNO from QCQuestion WITH (NOLOCK) order by QuestionNO"
		#distinguish question type:| 0,weak | 1,bad | 2,strong |
		QCQ = Raw.query_all( 'MSZ' )
		xml += "<QC>"

		for i in range( len( QCQ ) ):
			question = QCQ[i]
			if question[1]:
				xml += """<QCQuestion code = "%s" class="2" no = "%d" />""" % (
				question[0].decode( 'gbk' ), question[3] )
			elif question[2]:
				xml += """<QCQuestion code = "%s" class="1" no = "%d" />""" % (
				question[0].decode( 'gbk' ), question[3] )
			else:
				xml += """<QCQuestion code = "%s" class="0" no = "%d" />""" % (
				question[0].decode( 'gbk' ), question[3] )
		xml += "</QC>"

		#最初直接从packproc表中获取工序对应的员工姓名，因为两张表producestyle和producepackproc有关数据大多数情况下同步，但会有少数情况
		#存在有变动的情况修改了style表但是packproc表没有同步，但是员工姓名仍然存在于packproc表，所以变动查询方法 改动的时候没有
		Raw.sql = "select a.worklineno, a.workname, b.employee, b.employeeno from producestyle a left" \
		          " join producepackproc b WITH (NOLOCK) on a.worklineno = b.worklineno " \
		          "where a.producemasterid = '%s' and b.packid = '%s' and a.FlowInfoID<>'CF0E3C88-DB2F-4608-888B-5A19BA6FA7DC'" \
		          " order by a.worklineno" % ( info_ini['masterid'], info_ini['packid'] )

		workname_list = Raw.query_all( 'MSZ' )

		xml += "<PR>"
		if workname_list != False:
			for one in workname_list:
				xml += """<ProducePackProc WorkLineNo = "%d" WorkName = "%s" Employee = "%s" Employeeno = "%s" />""" % (
				one[0], one[1].decode( 'gbk' ), one[2], one[3] )

		xml += """<ProducePackProc WorkLineNo = "100" WorkName = "裁剪" Employee = "裁剪组" Employeeno = "0"/>""".decode(
			'utf-8' )
		xml += """<ProducePackProc WorkLineNo = "101" WorkName = "整烫" Employee = "整烫组" Employeeno = "0" />""".decode(
			'utf-8' )
		xml += """<ProducePackProc WorkLineNo = "0" WorkName = "未知" Employee = "未知" Employeeno = "0"/>""".decode(
			'utf-8' )
		xml += "</PR>"
		#if find in info table, add info in xml

		if info_ini['state'] == 2:
			xml += "<RC>"
			Raw.sql = "select a.serialno, a.employeeno, a.workname, a.workno, a.questionname, a.questionno, a.returnno," \
			          " a.employee, a.number_pack  from sklcc_info a join sklcc_record b on a.serialno = b.serialno" \
			          " where barcode = '%s' and a.batch = '%s' and b.inspector_no = '%s'" % ( barcode, info_ini['batch'], inspector_no )
			res_list = Raw.query_all( )
			returnno_sum = 0
			number_pack  = info_ini['number_pack']
			serialno     = res_list[0][0]
			for info_one in res_list:
				if info_one[6] == 0:
					xml += """</RC>"""
					Raw.sql = "delete from sklcc_info where barcode = '%s' and batch = '%s'" % (
					barcode, info_ini['batch'] )
					Raw.update( )
					return HttpResponse( xml )
				returnno_sum += info_one[6]
				xml += """<Record workname = "%s" workno = "%d" question ="%s" questionno = "%d" number = "%d" employee = "%s" employeeno = "%s"/>""" % (
				info_one[2], info_one[3], info_one[4], info_one[5], info_one[6], info_one[7], info_one[1] )
				#cause will be delete in info table, so update in Table table
				Raw.sql = "select returnno from sklcc_table where serialno = '%s' and employeeno = '%s' and questionno = %d" % (
					info_one[0], info_one[1], info_one[5] )
				Table_target = Raw.query_one( )
				returnno     = Table_target[0] - info_one[6]
					#if returnno = 0,then delete it,else update it
				if returnno == 0:
					Raw.sql = "delete from sklcc_table where serialno = '%s' and employeeno = '%s' and" \
					          " questionno = %d" % ( info_one[0], info_one[1], info_one[5] )
					Raw.update( )
				else:
					Raw.sql = "update sklcc_table set returnno = %d where serialno = '%s' and employeeno = '%s' and questionno = %d" % (
					returnno, info_one[0], info_one[1], info_one[5] )
					Raw.update( )


				#update record table

			Raw.sql = "select totalnumber, totalreturn from sklcc_record where serialno = '%s'" % serialno
			Record_target = Raw.query_one( )
			totalnumber   = Record_target[0]
			totalnumber  -= number_pack
			totalreturn   = Record_target[1]
			totalreturn  -= returnno_sum
			if totalnumber == 0:
				Raw.sql = "DELETE FROM sklcc_record WHERE serialno = '%s'"%serialno
			else:
				Raw.sql = "update sklcc_record set totalreturn = %d, totalnumber = %d where serialno = '%s'" % (
				totalreturn, totalnumber, serialno )
			Raw.update( )

				#delete in info table
			Raw.sql = "delete from sklcc_info where barcode = '%s'" % ( barcode )
			Raw.update( )
			xml += "</RC>"
		xml += """</xml>"""
		return HttpResponse( xml )
	except Exception, e:
		print e
		#logging.debug( e )

def update_info_new_but_slow( request ):
	try:
		Raw = Raw_sql( )
		inspector_no = request.session['employeeno']
		barcode = request.GET['code']
		xml = ""
		Raw.sql = "SELECT DBO.get_update_info_xml( '%s', '%s' )" % ( barcode, inspector_no )
		target = Raw.query_one( )
		if target != False:
			xml = target[0]
		Raw.sql = "EXEC pick_up_data_sync_sklcc_info_table_record '%s'" % barcode
		Raw.update( )
		return HttpResponse( xml )
	except Exception, e:
		logging.debug( e )


def get_employee( request ):
	departmentno = request.GET['group']
	employeeno = request.GET['no']
	Raw = Raw_sql( )
	Raw.sql = "select DepartmentNo, Employee from Employee WITH (NOLOCK) where employeeno = '%s'" % employeeno
	target = Raw.query_one( 'MSZ' )
	#找不到工号
	if target == False:
		return HttpResponse( '0' )
	#组别不对
	elif str( target[0] ) != departmentno:
		return HttpResponse( '1' + '@' + target[1] + '@' + employeeno )
	else:
		return HttpResponse( target[1] + '@' + employeeno )


#for xml example
def print_node( node ):
	print '================='
	print "node.attrib: %s" % node.attrib
	#prog,mist,
	if node.attrib.has_key( "prog" ) > 0:
		print "node.attrib['prog']:%s" % node.attrib['prog']
	print "node.tag:%s" % node.tag
	print "node.text:%s" % node.text


def written_info_in_database( serialno = "", barcode = "", check_id = 1, batch = "", departmentno = "", workno = 0,
                              questionno = 0, number_pack = 0, returnno = 0, inspector_no = "", inspector = "",
                              employeeno = "", employee = "", request = None ):
	reload( sys )
	sys.setdefaultencoding( 'utf-8' )

	Raw = Raw_sql( )
	if request != None:
		if barcode != 'null':
			try:
				Raw.sql = "insert into sklcc_info ( state, returnno, barcode, boxno, batch, number_pack, serialno ) values( %d, %d, '%s', %d, '%s', %d, '%s' )" % (
				2, 0, barcode, int( barcode[6:10] ), batch, number_pack, serialno )
				Raw.update( )
			except Exception, e:
				make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) + '|' + str( barcode ) + '|' + str(
					request.session['employeeno'] ) + '|' + 'barcodenull' )
		else:
			Raw.sql = "insert into sklcc_info ( state, returnno, barcode, boxno, batch, number_pack, serialno ) values( %d, %d, '%s', %d, '%s', %d, '%s' )" % (
			2, 0, barcode, 0, batch, number_pack, serialno )
			Raw.update( )
		temp = temp_Info( )
		temp.barcode = barcode
		temp.serialno = serialno
		temp.batch = batch
		temp.departmentno = departmentno
		temp.inspector_no = inspector_no
		temp.inspector = inspector
		temp.check_id = check_id
		temp.check_type = get_check_type( check_id )
		return temp

	Raw.sql = "select QuestionCode, isStrong, isBad from QCQuestion WITH (NOLOCK) where QuestionNO = %d" % int(
		questionno )
	questionname = Raw.query_one( 'MSZ' )[0]
	#unknow program
	if workno == 0:
		workname = "unknown"
		workno = 0
		if check_id == '1':
			employee = "unknown"
			employeeno = "unknown"
	elif workno == 100:
		workname = "裁剪".encode( 'gbk' )
		workno = 100
		employee = "裁剪组"
		employeeno = "裁剪组"
	elif workno == 101:
		workname = "整烫".encode( 'gbk' )
		workno = 101
		employee = "整烫组"
		employeeno = "整烫组"
	else:
		info_ini = get_info( barcode, inspector_no )
		Raw.sql = "select WorkName from ProducePackProc WITH (NOLOCK) where ( PackID = '" + str(
			info_ini['packid'] ) + "') and WorkLineNo = %d" % int( workno )
		target_sec = Raw.query_one( 'MSZ' )
		workname = target_sec[0]
		workno = int( workno )
	#isstrong
	questiontype = get_question_type( questionno )

	returnno = int( returnno )
	barcode = barcode
	boxno = int( barcode[6:10] ) if barcode != 'null' else 0
	number_pack = number_pack
	questionno = int( questionno )
	questionname = questionname.decode( 'gbk' )
	workname = workname.decode( 'gbk' )
	barcode = barcode.decode( 'gbk' )
	batch = batch

	Raw.sql = "insert into sklcc_info values( %d, '%s',%d, %d, '%s', %d, '%s', '%s', %d, '%s', %d, %d, '%s', '%s'  )" % (
	2, questionname, questionno, questiontype, workname, workno, employee, employeeno, returnno, barcode, boxno,
	number_pack, serialno, batch )
	Raw.update( )
	temp = temp_Info( )
	temp.state = 2
	temp.check_id = check_id
	temp.questionname = questionname
	temp.questionno = questionno
	temp.workname = workname
	temp.workno = workno
	temp.employee = employee
	temp.employeeno = employeeno
	temp.type_data = questiontype
	temp.returnno = returnno
	temp.barcode = barcode
	temp.boxno = boxno
	temp.number_pack = number_pack
	temp.serialno = serialno
	temp.batch = batch
	temp.departmentno = departmentno
	temp.inspector = inspector
	temp.inspector_no = inspector_no
	temp.check_type = get_check_type( check_id )
	return temp


def written_table_in_database( temp ):
	reload( sys )
	sys.setdefaultencoding( 'utf-8' )
	table = Raw_sql( )
	table.sql = u"select returnno from sklcc_table where serialno = '%s' and employeeno = '%s' and workno = '%s' and questionno = %d" % (
	temp.serialno, temp.employeeno, temp.workno, int( temp.questionno ) )
	#table_record = Table.objects.get( serialno = temp.serialno, employeeno = temp.employeeno, workno = temp.workno, questionno = temp.questionno )
	#except Table.DoesNotExist:

	target = table.query_one( )
	if target == False:
		try:
			serialno = temp.serialno
			state = 2
			workname = temp.workname
			workno = int( temp.workno )
			returnno = int( temp.returnno )
			questionname = temp.questionname
			questionno = int( temp.questionno )
			questiontype = get_question_type( questionno )
			employee = temp.employee
			employeeno = temp.employeeno
			table.sql = "insert into sklcc_table values ( '%s', %d, '%s', '%s', '%s', %d, %d, %d, '%s', %d )" % (
			serialno, state, employeeno, employee, workname, workno, returnno, questionno, questionname, questiontype )
			#print table.sql
			table.update( )
		except Exception, e:
			make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) + '|' + str( temp.barcode ) + '|' + str(
				temp.employeeno ) + '|' + 'tablewritten' + '|' )
	#have written in this table, then update it
	else:
		returnno = target[0] + int( temp.returnno )
		table.sql = "update sklcc_table set returnno = %d where serialno = '%s' and employeeno = '%s' and workno = %d and questionno = %d" % (
		returnno, temp.serialno, temp.employeeno, int( temp.workno ), int( temp.questionno ) )
		#table_record.update(returnno = returnno) can't work
		table.update( )
	#if not have written in table about this serialno, employeeno and questionno,then write in


def written_record_in_database( temp ):
	Raw = Raw_sql( )
	em_number = temp.inspector_no
	Raw.sql = "select * from sklcc_record where serialno = '%s'" % temp.serialno
	target = Raw.query_one( )

	#if find in record table, then update totalnumber and totalreturnno, else make a record
	if target == False:

		serialno = temp.serialno
		T = Current_time( )
		createtime = T.time_str
		inspector = temp.inspector
		inspector_no = temp.inspector_no
		state = 2
		totalnumber = get_record_totalnumber( temp.serialno )
		batch = temp.batch
		totalreturn = get_record_totalreturn( temp.serialno )
		departmentno = temp.departmentno

		Raw.sql = "insert into sklcc_record( serialno, createtime, inspector, inspector_no, state, totalnumber, departmentno, batch, totalreturn, check_id, check_type )" \
		          " values( '%s', '%s', '%s', '%s', %d, %d, '%s', '%s', %d, '%s', '%s' )" % (
		          serialno, createtime, inspector, inspector_no, state, totalnumber, departmentno, batch, totalreturn,
		          temp.check_id, temp.check_type )
		Raw.update( )
	else:
		totalnumber = get_record_totalnumber( temp.serialno )
		totalreturn = get_record_totalreturn( temp.serialno )
		Raw.sql = "update sklcc_record set totalnumber = %d, totalreturn = %d where serialno = '%s'" % (
		totalnumber, totalreturn, temp.serialno )
		Raw.update( )


def written_return_check_in_datebase( temp, check_type ):
	Raw = Raw_sql( )
	Raw.sql = "select * from sklcc_return_check where serialno = '%s'" % temp.serialno
	target = Raw.query_all( )
	if target == False:
		Raw.sql = "insert into sklcc_return_check( serialno, real_return, ok, state )" \
		          " values( '%s',  %d, %d, %d )" % ( temp.serialno, 0, 1, 0  )
		Raw.update( )


def get_return_percentage( departmentno, date ):
	try:
		Raw = Raw_sql( )
		Raw.sql = "select sum( totalreturn ), sum( totalnumber ) from sklcc_record where left( createtime, 10 ) = '%s' and departmentno = '%s'" % (
		date, departmentno )
		totalnumber = 0
		totalreturn = 0
		target = Raw.query_one( )
		if target != False:
			if target[0] != None and target[1] != None:
				totalnumber = target[1]
				totalreturn = target[0]

		return round( float( totalreturn ) / float( totalnumber ), 4 ) if int( totalnumber ) != 0 else 0
	except Exception, e:
		make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )


def get_common_difference( styleno, partition ):
	Raw = Raw_sql( )
	Raw.sql = "select common_difference from sklcc_style_measure where styleno = '%s' and partition = '%s'" % (
	styleno, partition )
	target = Raw.query_one( )

	if target != False:
		return target[0]
	else:
		return 0

def get_symmetry( styleno, partition ):
	Raw = Raw_sql( )
	Raw.sql = "select symmetry from sklcc_style_measure where styleno = '%s' and partition = '%s'" % (
	styleno, partition )
	target = Raw.query_one( )

	if target != False:
		return target[0]
	else:
		return 0


def get_measure_res( styleno, partition ):
	Raw = Raw_sql( )
	Raw.sql = "select measure_res from sklcc_style_measure where styleno = '%s' and partition = '%s'" % (
	styleno, partition )
	target = Raw.query_one( )

	if target != False:
		return target[0]
	else:
		return 0


def prase_measure_json( barcode, serialno, styleno, departmentno, size, inspector_no, batch, measure_json ):
	T = Current_time( )
	now = T.time_str
	insert_list = []
	temp = { }
	temp['barcode'] = barcode
	temp['serialno'] = serialno
	temp['styleno'] = styleno
	temp['size'] = size
	temp['batch'] = batch
	temp['createtime'] = now
	temp['inspector_no'] = inspector_no
	temp['departmentno'] = departmentno
	for one in measure_json:
		temp['partition'] = one['name']
		res = one['res']
		for id, count in enumerate( res ):
			temp['id'] = id + 1
			if len( count ) != 1:
				temp['symmetry1'] = float( count[0] )
				temp['symmetry2'] = float( count[1] )
				temp['measure_type'] = 1
			else:
				temp['measure_res'] = float( count[0] )
				temp['measure_type'] = 2
			insert_list.append( copy.deepcopy( temp ) )

	return insert_list




def commit_res( request ):
	try:
		reload( sys )
		sys.setdefaultencoding( 'utf-8' )
		Raw = Raw_sql( )
		insert_info = dict( )
		SQL = ""

		insert_info['barcode'] = request.POST.get( 'codenumber' )
		insert_info['batch'] = request.POST.get( 'batch' )
		insert_info['batch'] = request.POST.get( 'batch' )
		insert_info['number_pack'] = int( request.POST.get( 'count' ) )
		insert_info['departmentno'] = request.POST.get( 'group' )
		insert_info['inspector'] = request.POST.get( 'inspectorname' )
		insert_info['inspector_no'] = request.POST.get( 'inspectorno' )
		insert_info['check_id'] = request.POST.get( 'type' )
		insert_info['res'] = list( )
		totalreturn = 0

		json = simplejson.loads( request.POST.get( 'res_json' ) )
		T = Current_time( )
		today = T.get_date( )

	##TODO:fix this problem measure
		Raw.sql = "select serialno, measure_count from sklcc_measure_record where inspector_no = '%s' " \
		          "and left( createtime, 10 ) = '%s' and batch = '%s' and size = [BDDMS_MSZ].DBO.get_size_by_barcode( '%s' )"\
		          % ( insert_info['inspector_no'], today, insert_info['batch'], insert_info['barcode'] )
		target = Raw.query_one( )
		if target == False:
			serialno = uuid.uuid1( )
			createtime = T.time_str
			Raw.sql = u"SELECT TOP 1 a.styleno, b.size FROM ProduceMaster a JOIN producepack b WITH (NOLOCK) " \
			          u"ON a.producemasterid = b.producemasterid WHERE Barcode = SUBSTRING('%s',1,5)" \
			          u" AND FormState = '审核' AND packno = SUBSTRING( '%s', 6, 5 )"%( insert_info['barcode'], insert_info['barcode'] )
			style = Raw.query_one('MSZ')
			if style != False:
				written_into_measure_record(
				dict( serialno = serialno, createtime = createtime, inspector_no = insert_info['inspector_no'],
				    inspector = insert_info['inspector'], batch = insert_info['batch'], styleno = style[0], size = style[1],
			         measure_count = 0 ) )
		Raw.sql = u"select serialno from sklcc_record where state = 2 and batch = '%s' and inspector_no = '%s' and" \
		          u" check_id = '%s' and left( createtime, 10 ) = '%s'" % (
		          insert_info['batch'], insert_info['inspector_no'], insert_info['check_id'], today )
		target = Raw.query_one( )
		if target == False:
			insert_info['serialno'] = unicode( uuid.uuid1( ) )
			is_serialno_new = True
		else:
			insert_info['serialno'] = target[0]
			is_serialno_new = False

		if len( json ) != 0:
			for item in json:
				SQL += u"""insert into sklcc_info( state, questionname, questionno, type, workname, workno, employee,
 	    					employeeno, returnno, barcode, boxno, number_pack, serialno, batch )
 	    					values( 2, [BDDMS_MSZ].DBO.get_questioncode_by_no( %d ),%d, [BDDMS_MSZ].DBO.get_questiontype_by_no( %d ),
 	    		[BDDMS_MSZ].DBO.get_workname_by_worklineno_and_barcode( %d, '%s' ), %d, '%s', '%s', %d, '%s', %d, %d, '%s', '%s'); """ % (
				int( item['mistake_no'] ), int( item['mistake_no'] ), int( item['mistake_no'] ), int( item['work_no'] ),
				insert_info['barcode'], int( item['work_no'] ), item['employee_name'], item['employee_no'],
				int( item['count'] ), insert_info['barcode'], int( insert_info['barcode'][5:] ),
				insert_info['number_pack'], insert_info['serialno'], insert_info['batch'] )
				totalreturn += int( item['count'] )
			#SQL = SQL[:-10] + ';' #去除最后一个UNION ALL 并且加上执行分号
		else:
			SQL = u"insert into sklcc_info ( state, returnno, barcode, boxno, batch, number_pack, serialno )" \
			      u" values( 2, 0, '%s', %d, '%s', %d, '%s' );" % (
			      insert_info['barcode'], int( insert_info['barcode'][5:] ), insert_info['batch'],
			      insert_info['number_pack'], insert_info['serialno'] )
		####    ###################################        sklcc info table     ####################################################

		####    ###################################        sklcc record table   ####################################################
		if is_serialno_new:
			SQL += u"insert into sklcc_record( serialno, createtime, inspector, inspector_no, state, totalnumber," \
			       u" departmentno, batch, totalreturn, check_id, check_type )" \
			       u" values( '%s', '%s', '%s', '%s', %d, %d, '%s', '%s', %d, '%s', DBO.get_check_type_by_check_id( '%s' ));" % (
			       insert_info['serialno'], T.time_str, insert_info['inspector'], insert_info['inspector_no'], 2,
			       insert_info['number_pack'], insert_info['departmentno'], insert_info['batch'], totalreturn,
			       insert_info['check_id'], insert_info['check_id'] )
			SQL += u"insert into sklcc_return_check( serialno, real_return, ok, state )" \
			       " values( '%s',  0, 1, 0 )" % ( insert_info['serialno'] )
		else:
			SQL += u"update sklcc_record set totalnumber = dbo.get_totalnumber_by_serialno( '%s' )," \
			       u" totalreturn = (SELECT sum( returnno ) FROM sklcc_info WHERE serialno =  '%s' ) " \
			       u"where serialno = '%s';" % (
			       insert_info['serialno'], insert_info['serialno'], insert_info['serialno'] )

		Raw.sql = SQL
		Raw.update( )
		return HttpResponse( )

	except Exception, e:
		logging.debug(e)


def commit_res_old( request ):
	try:
		reload( sys )
		sys.setdefaultencoding( 'utf-8' )
		barcode = request.POST.get( 'codenumber' )
		batch = request.POST.get( 'batch' )
		number_pack = int( request.POST.get( 'count' ) )
		departmentno = request.POST.get( 'group' )
		inspector = request.POST.get( 'inspectorname' )
		inspector_no = request.POST.get( 'inspectorno' )
		check_id = request.POST.get( 'type' )
		check_id = request.POST.get( 'type' )
		res = request.POST.get( 'xml' )
		root = ElementTree.fromstring( res )
		node = root.getiterator( "re" )
		styleno = batch.split( '-' )[0]
		size = request.POST['size'] if 'size' in request.POST else ""
		temp = temp_Info( )
		T = Current_time( )
		Raw = Raw_sql( )
		today = T.get_date( )

		Raw.sql = "select serialno from sklcc_record where state = 2 and batch = '%s' and inspector_no = '%s' and check_id = '%s' and left( createtime, 10 ) = '%s'" % (
		batch, inspector_no, check_id, today )
		target = Raw.query_one( )
		if target == False:
			serialno = str( uuid.uuid1( ) )
		else:
			serialno = target[0]


		#if not any question in a box, also need to save data in database
		if len( node ) == 0:
			temp = written_info_in_database( serialno = serialno, batch = batch, number_pack = number_pack,
			                                 check_id = check_id, departmentno = departmentno,
			                                 inspector_no = inspector_no, inspector = inspector, barcode = barcode,
			                                 request = request )
		else:
			#unique employeeno, unique prog
			for node_t in node:
				workno = int( node_t.attrib['prog'] )
				question = int( node_t.attrib['mist'] )
				returnno = int( node_t.attrib['count'] )
				employee = node_t.attrib['employee']
				employeeno = node_t.attrib['employeeno']

				#to do:make written_record_in_database out of the for loop
				temp = written_info_in_database( serialno, barcode, check_id, batch, departmentno, workno, question,
				                                 number_pack, returnno, inspector_no, inspector, employeeno, employee )

				#written_record_in_database( temp )
				written_table_in_database( temp )
		written_record_in_database( temp )
		written_return_check_in_datebase( temp, 1 )

		T = Current_time( )
		Raw = Raw_sql( )
		Raw.sql = "select EQ_return_percentage from sklcc_config"
		EQ_return_percentage = 0.0
		target_list = Raw.query_all( )
		if target_list != False:
			EQ_return_percentage = target_list[0][0]

		return_percentage = get_return_percentage( temp.departmentno, T.get_date( ) ) * 100
		mes = str( return_percentage ) + '%'
		if ( return_percentage - EQ_return_percentage ) > 1e-6:
			message = '当前返修率过高@@@返修率:%s@@@当前统计数据截止到%s#0' % ( mes, T.get_time( )[0:8] )
			imsend( temp.departmentno, '300', message.decode( 'utf-8' ), '1', '0' )

		if inspector_no != request.session['employeeno']:
			update_all_state_to( temp.serialno, 1 )
		return HttpResponse( )
	except Exception, e:
		make_log(
			sys._getframe( ).f_code.co_name + ">>>" + str( e ) + '|' + str( request.POST.get( 'codenumber' ) ) + '|' +
			request.session['employee'] + '|' )


def get_check_type( check_id ):
	Raw = Raw_sql( )
	Raw.sql = "select check_type from sklcc_check_type where check_id = '%s'" % check_id
	target = Raw.query_one( )
	return target[0] if target else False


def get_all_partition( measure_type_id ):
	res = []
	Raw = Raw_sql( )
	Raw.sql = "select partition from sklcc_measure_partition where measure_type_id = '%s'" % measure_type_id
	target_list = Raw.query_all( )
	if target_list != False:
		for target in target_list:
			res.append( target[0] )
	return res


def style_measure( request ):
	try:
		if 22 not in request.session['status']:
			return HttpResponseRedirect( '/warning/' )
		#reload(sys)
		#sys.setdefaultencoding('utf-8')
		em_number    = request.session['employeeno']
		employeename = request.session['employee']
		Raw = Raw_sql( )
		Raw.sql = "select measure_type_id, measure_type_name from sklcc_measure_type"
		target_list = Raw.query_all( )
		measure_list = []
		state = 0
		if target_list != False:
			for target in target_list:
				temp = { 'id': target[0], 'name': target[1] }
				partiton_list = get_all_partition( target[0] )
				temp['partition_list'] = partiton_list
				measure_list.append( temp )
		html = get_template( 'measure_size_set.html' )
		measure_list_json = simplejson.dumps( measure_list, ensure_ascii = False )

		if 'style' in request.GET:
			style = request.GET['style']
			if style == '':
				state = 0
				return TemplateResponse( request, html, locals( ) )

			Raw.sql = "select distinct partition, serial from sklcc_style_measure where styleno = '%s' ORDER BY serial" % style
			target_list = Raw.query_all( )
			if target_list == False:
				state = 1
				return TemplateResponse( request, html, locals( ) )
			else:
				res = []
				for target in target_list:
					temp = { }
					size_list = []
					Raw.sql = "select common_difference, createtime, symmetry, size, partition, measure_res, measure_or_not, note" \
					          " from sklcc_style_measure where styleno = '%s' and partition = '%s' order by size" % (
					          style.decode( 'utf-8' ), target[0] )
					info_list = Raw.query_all( )
					if info_list != False:
						temp['common'] = str( info_list[0][0] ) if info_list[0][0] != 0 else ''
						temp['symmetry'] = str( info_list[0][2] ) if info_list[0][0] != 0 else ''
						temp['partition'] = target[0]
						temp['hint'] = info_list[0][7].decode( "gbk" ) if info_list[0][7] != None else ''
						temp['measure_or_not'] = 1 if info_list[0][6] else 0
						temp['data'] = []
						for info in info_list:
							one = { }
							one['size'] = info[3]
							size_list.append( info[3] )
							one['no'] = str( info[5] ) if info[5] != 0 else ''
							temp['data'].append( one )
					res.append( temp )
				state = 2
		return TemplateResponse( request, html, locals( ) )
	except Exception, e:
		print e
		logging.debug( e )


def written_into_style_measure( record ):
	Raw = Raw_sql( )
	T = Current_time( )
	now = T.time_str
	Raw.sql = u"insert into sklcc_style_measure( employeeno,serial,styleno, common_difference, createtime, symmetry, size, partition, " \
	          u"measure_res, note, measure_or_not  ) values( '%s', '%d', '%s', %f, '%s', %f, '%s', '%s', %f, '%s', " % (
	          record['employeeno'], record['index'], record['styleno'], record['common_difference'], now, record['symmetry'], record['size'],
	          record['partition'], record['number'], record['note'] )
	Raw.sql += '1 )' if record['measure_or_not'] == True else '0 )'
	Raw.update( )


def submit_style_measure( request ):
	try:
		reload( sys )
		sys.setdefaultencoding( 'utf-8' )
		Raw = Raw_sql( )
		json = request.POST.get('json')
		res = simplejson.loads( json )
		if res['new_style'] != res['old_style']:
			Raw.sql = "select * from sklcc_style_measure where styleno = '%s'" % res['new_style']
			target = Raw.query_one( )
			if target != False:
				#this new styleno has been found
				return HttpResponse( '0' )

		Raw.sql = "delete from sklcc_style_measure where styleno = '%s'" % res['old_style']
		Raw.update( )
		record = { }
		record['styleno']    = res['new_style']
		record['employeeno'] = request.session['employeeno']
		data = res['data']
		for one in data:
			print one
			record['partition']         = one['name']
			record['index']             = int( one['index'] )
			record['measure_or_not']    = one['is_need']
			record['note']              = one['hint']
			record['symmetry']          = float( one['balance_error'] ) if one['balance_error'] != None else 0
			record['common_difference'] = float( one['common_difference'] ) if one['common_difference'] != None else 0
			for temp in one['res']:
				if temp.has_key( 'size' ):
					record['size'] = temp['size']
					record['number'] = float( temp['data'] ) if temp['data'] != None else 0
					written_into_style_measure( record )
				else:
					break

		return HttpResponse( '1' )
	except Exception, e:
		print e
		make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )


##################################### *@*       end of dataentry        *@* ############################################

#################################### *@*       start of choose and check        *@* ####################################

def update_all_state_to( serialno, state, is_measure = False ):
	Raw = Raw_sql( )
	if is_measure == False:
		Raw.sql = "select * from sklcc_record where serialno = '%s'" % serialno
		target_record = Raw.query_one( )

		if target_record == False:
			return False
		else:
			Raw.sql = "update sklcc_record set state = %d where serialno = '%s'" % ( state, serialno )
			Raw.update( )

		Raw.sql = "select * from sklcc_table where serialno = '%s'" % serialno
		target_table = Raw.query_all( )
		if target_table == False:
			return False
		else:
			Raw.sql = "update sklcc_table set state = %d where serialno = '%s'" % ( state, serialno )
			Raw.update( )

		Raw.sql = "select TOP 1 * from sklcc_info where serialno = '%s'" % serialno
		target_info = Raw.query_all( )
		if target_info == False:
			return False
		else:
			Raw.sql = "update sklcc_info set state = %d where serialno = '%s'" % ( state, serialno )
			Raw.update( )
	else:
		Raw.sql = "update sklcc_measure_record set state = %d where serialno = '%s'" % ( state, serialno )
		Raw.update( )


def find_table_with_serialno( serialno ):
	table = Raw_sql( )
	table.sql = "select * from sklcc_table where serialno = '%s'" % serialno
	table_list = table.query_all( )
	return table_list


def find_measure_record_state_is_help_function( raw_SQL, state, is_first_check = True ):
	Raw = Raw_sql( )
	Raw.sql = raw_SQL
	reco_list = Raw.query_all( )
	record_list = list( )

	if reco_list != False:
		for reco in reco_list:
			createtime = reco[1].split( '.' )[0]
			string = str( createtime ).split( ' ' )[0].split( '-' )
			year = int( string[0] )
			month = int( string[1] )
			day = int( string[2] )

			createtime_form = datetime.datetime( year, month, day )
			Raw = Raw_sql( )
			Raw.sql = "select days from sklcc_config"
			target = Raw.query_one( )
			if (datetime.datetime.today( ) - createtime_form).days > target[0]:
				continue
			record = Record_info( )
			record.createtime = reco[1].split( '.' )[0][5:-3]
			record.serialno = reco[0]
			record.inspector = reco[2]
			record.inspector_no = reco[3]
			record.state = reco[4]
			record.assessor = reco[5]
			record.assessor_no = reco[6]
			record.assesstime = reco[7].split( '.' )[0][5:-3] if reco[7] != None else ''
			record.departmentno = reco[8]
			record.batch = reco[9]
			record.totalnumber = reco[11]
			record.totalreturn = -1
			#normal_check 0 partition_measure 1
			record.check_id = 1
			record.check_type = "部位测量"
			if state == 2:
				if is_first_check:
					record.url = "/table_measure/?serialno=%s&state=%d#first" % ( record.serialno, record.state )
				else:
					record.url = "/table_measure/?serialno=%s&state=%d#second" % ( record.serialno, record.state )
			else:
				if is_first_check:
					record.url = "/table_measure_read_only/?serialno=%s&state=%d#first" % (
					record.serialno, record.state )
				else:
					record.url = "/table_measure_read_only/?serialno=%s&state=%d#second" % (
					record.serialno, record.state )
			record_list.append( record )
	return record_list


#control = 0, have reject,pass; control = 1, not have...
def find_record_state_is( state, employeeno, authority_in_use, control ):
	Raw = Raw_sql( )
	record_list = []
	#choose: 2
	if authority_in_use == 2:
		#off the authority control
		#departmentno_list = find_department_authority_user( username, 2 )
		#for departmentno in departmentno_list:
		Raw.sql = '''SELECT check_type, SUBSTRING(createtime,6,11) time, state, batch,
 							totalnumber, totalreturn, serialno, departmentno, inspector, inspector_no,
					( SELECT COUNT(*) FROM sklcc_info WHERE type = 0 AND serialno = record.serialno ) AS weak,
					( SELECT COUNT(*) FROM sklcc_info WHERE type = 1 AND serialno = record.serialno ) AS bad,
					( SELECT COUNT(*) FROM sklcc_info WHERE type = 2 AND serialno = record.serialno ) AS strong
					FROM sklcc_record record
					WHERE inspector_no = '%s' AND state = %d AND createtime > ( SELECT dbo.get_date_before_config_days() )
					ORDER BY id DESC ''' % ( employeeno, state )
	#choose_check
	elif authority_in_use == 4:
		Raw.sql = '''SELECT check_type, SUBSTRING(createtime,6,11) time, state, batch,
 							totalnumber, totalreturn, serialno, departmentno, inspector, inspector_no,
					( SELECT COUNT(*) FROM sklcc_info WHERE type = 0 AND serialno = record.serialno ) AS weak,
					( SELECT COUNT(*) FROM sklcc_info WHERE type = 1 AND serialno = record.serialno ) AS bad,
					( SELECT COUNT(*) FROM sklcc_info WHERE type = 2 AND serialno = record.serialno ) AS strong
					FROM sklcc_record record
					WHERE state = %d
					AND createtime > ( SELECT dbo.get_date_before_config_days() )
					AND departmentno IN
          			( SELECT departmentno FROM sklcc_employee_authority
            			WHERE authorityid = 4 AND username = '%s' )
					ORDER BY id DESC ''' % ( state, employeeno )
	target_list = Raw.query_all( )

	if target_list != False:
		for target in target_list:
			record = { 'check_type': target[0], 'createtime': target[1], 'state': target[2], 'batch': target[3],
			           'totalnumber': target[4], 'totalreturn': target[5], 'serialno': target[6],
			           'departmentno': target[7], 'inspector': target[8], 'inspector_no': target[9] }
			if state == 2 or state == 3:
				if control == 1:
					record['url'] = "/table?%d#%s/" % ( target[2], target[6] )
				else:
					record['url'] = "/read_only_table?%d#%s/" % ( target[2], target[6] )
			else:
				if control == 1:
					record['url'] = "/check?%d#%s/" % ( target[2], target[6] )
				else:
					record['url'] = "/read_only_table?%d#%s/" % ( target[2], target[6] )
			record_list.append( copy.deepcopy( record ) )

	return record_list


def sync_table_from_record( serialno ):
	totalreturn = get_record_totalreturn( serialno )
	Raw = Raw_sql( )
	Raw.sql = "update sklcc_record set totalreturn = %d where serialno = '%s'" % ( totalreturn, serialno )
	Raw.update( )


def count_type( serialno ):
	SQL = Raw_sql( )
	SQL.sql = "select questiontype, returnno from sklcc_table where serialno = '%s'" % serialno
	target_list = SQL.query_all( )
	if target_list == False:
		return False

	count = type_count_three( )
	for target in target_list:
		if target[0] == 0:
			count.weak += target[1]
		elif target[0] == 1:
			count.bad += target[1]
		else:
			count.strong += target[1]
	return count


def get_question_type( questionno ):
	question = Raw_sql( )
	question.sql = "select isStrong, isBad from QCQuestion WITH (NOLOCK) where QuestionNO = %d" % questionno
	target = question.query_one( 'MSZ' )

	if target == False:
		return None
	if target[0] == True:
		return 2
	elif target[1] == True:
		return 1
	else:
		return 0


def tables_xml( record ):
	xml = """<xml>"""
	xml += """<info>"""
	xml += """<group>%s</group>""" % record['departmentno']
	xml += """<count>%d</count>""" % record['totalnumber']
	xml += """<date>%s</date>""" % record['createtime'].split( '.' )[0]
	xml += """<no>%s</no>""" % record['batch']
	xml += """<inspector>%s</inspector>""" % record['inspector']
	xml += """<inspector_no>%s</inspector_no>""" % record['inspector_no']
	xml += """<check_type>%s</check_type>""" % record['check_type']
	xml += """</info>"""

	if record['totalreturn'] == 0:
		xml += """</xml>"""
		return xml
	xml += """<RC>"""
	xml_weak = """"""
	xml_bad = """"""
	xml_strong = """"""

	RC_list = find_table_with_serialno( record['serialno'] )
	for RC in RC_list:
		if RC[10] == 0:
			xml_weak += """<record0 name = '%s' no = '%d' employee_name = '%s' employee_no = '%s' count = '%d' program_no = '%d' program_name = '%s' />""" % (
			RC[9], RC[8], RC[4], RC[3], RC[7], RC[6], RC[5] )
		elif RC[10] == 1:
			xml_bad += """<record1 name = '%s' no = '%d' employee_name = '%s' employee_no = '%s' count = '%d' program_no = '%d' program_name = '%s' />""" % (
			RC[9], RC[8], RC[4], RC[3], RC[7], RC[6], RC[5] )
		else:
			xml_strong += """<record2 name = '%s' no = '%d' employee_name = '%s' employee_no = '%s' count = '%d' program_no = '%d' program_name = '%s' />""" % (
			RC[9], RC[8], RC[4], RC[3], RC[7], RC[6], RC[5] )

	xml += xml_weak
	xml += xml_bad
	xml += xml_strong
	xml += """</RC>"""
	xml += """</xml>"""

	return xml


def commit_table( request ):
	try:
		xml = request.POST['xml']
		reload( sys )
		sys.setdefaultencoding( 'utf-8' )
		root = ElementTree.fromstring( xml )
		serialno = root.getiterator( "no" )[0].text
		if 'is_measure' in request.GET:
			if request.GET['is_measure'] == '1':
				#return is a list
				save_table( request, True )
				update_all_state_to( serialno, 0, True )
			else:
				save_table( request )
				update_all_state_to( serialno, 0 )
		else:
			save_table( request )
			update_all_state_to( serialno, 0 )
		return HttpResponse( )
	except Exception, e:
		make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )


def delete_record( request ):
	Raw = Raw_sql( )
	serialno = request.GET['serial']
	is_measure = request.GET['is_measure'] if 'is_measure' in request.GET else '0'
	if is_measure == '1':
		Raw.sql = "delete from sklcc_measure_info where serialno = '%s'" % serialno
		Raw.update( )
		Raw.sql = "delete from sklcc_measure_record where serialno = '%s'" % serialno
		Raw.update( )
	else:
		Raw.sql = "delete from sklcc_info where serialno = '%s'" % serialno
		Raw.update( )

		Raw.sql = "delete from sklcc_table where serialno = '%s'" % serialno
		Raw.update( )

		Raw.sql = "delete from sklcc_record where serialno = '%s'" % serialno
		Raw.update( )

		Raw.sql = "delete from sklcc_return_check where serialno = '%s'" % serialno
		Raw.update( )
	return HttpResponse( 1 )


def tables( request ):
	status = request.session['status']
	if 2 in status:
		username = request.session['username']
		em_number = request.session['employeeno']
		html = get_template( 'tables.html' )
		return TemplateResponse( request, html )
	else:
		return HttpResponseRedirect( '/warning/' )


#tables in /choose/
def update_table( request ):
	state = int( request.GET['state'] )
	username = request.session['username']
	record_list = find_record_state_is( state, username, 2, 0 )
	xml = """"""
	try:
		for record in record_list:
			if request.GET['code'] == record['serialno']:
				xml = tables_xml( record )
	except Exception, e:
		logging.debug( e )
	return HttpResponse( xml )


#tables in /choose_check/
def update_table_check( request ):
	Raw = Raw_sql( )
	state = int( request.GET['state'] )
	serialno = request.GET['code']

	Raw.sql = "select departmentno, totalnumber, createtime, batch, inspector," \
	          " inspector_no, check_type, totalreturn, serialno from sklcc_record where serialno = '%s'" \
	          " and state = %d" % ( serialno, state )

	target = Raw.query_one( )
	xml = """"""
	try:
		if target != False:
			record = dict( )
			record['departmentno'] = target[0]
			record['totalreturn'] = target[7]
			record['totalnumber'] = target[1]
			record['createtime'] = target[2]
			record['batch'] = target[3]
			record['inspector'] = target[4]
			record['inspector_no'] = target[5]
			record['check_type'] = target[6]
			record['serialno'] = target[8]
			xml = tables_xml( record )
		return HttpResponse( xml )
	except  Exception, e:
		logging.debug( e )


def choose( request ):

	status = request.session['status']
	if 2 in status:
		html = get_template( 'choose.html' )
		username = request.session['username']
		em_number = request.session['employeeno']
		employeename = request.session['employee']
		date = Current_time.get_now_date( )
		url = '/return_check/?start=%s&end=%s' % ( date, date )

		record_not_commit_list = find_record_state_is( 2, username, 2, 1 )
		record_have_committed_list = find_record_state_is( 1, username, 2, 0 )
		record_have_committed_list = find_record_state_is( 0, username, 2, 0 ) + record_have_committed_list
		return TemplateResponse( request, html,
		                         { 'username': username, 'em_number': em_number, 'employeename': employeename,
		                           'date': date, 'url': url, 'record_not_commit_list': record_not_commit_list,
		                           'record_have_committed_list': record_have_committed_list } )
	else:
		return HttpResponseRedirect( '/warning/' )


def save_table( request, is_measure = False ):
	if is_measure == False:
		try:
			Raw = Raw_sql( )
			xml = request.POST['xml']
			reload( sys )
			sys.setdefaultencoding( 'utf-8' )
			root = ElementTree.fromstring( xml )
			#return is a list
			serialno = root.getiterator( "no" )[0].text
			state = root.getiterator( "state" )[0].text
			if state == '0':
				return HttpResponse( )
			else:
				record_list = root.getiterator( "record" )
				for record in record_list:
					workno = int( record.attrib['program_no'] )
					questionno = int( record.attrib['mistake_no'] )
					count = int( record.attrib['count'] )
					employeeno = record.attrib['employee_no']
					questionname = record.attrib['mistake_name']
					workname = record.attrib['program_name']
					employee = record.attrib['employee_name']
					Raw.sql = "select * from sklcc_table where serialno = '%s' and workno = %d and questionno = %d" % (
					serialno, workno, questionno )
					target = Raw.query_one( )
					if target == False:
						if count == 0:
							pass
						else:
							Raw.sql = "select state from sklcc_table where serialno = '%s' and workno = %d" % (
							serialno, workno )
							target = Raw.query_one( )
							Raw.sql = "insert into sklcc_table values ( '%s', %d, '%s', '%s', '%s', %d, %d, %d, '%s', %d )" % (
							serialno, target[0], employeeno, employee, workname, workno, count, questionno,
							questionname, get_question_type( questionno ) )
							Raw.update( )
					else:
						if count == 0:
							Raw.sql = "delete from sklcc_table where serialno = '%s' and workno = %d and questionno = %d and employeeno = '%s'" % (
							serialno, workno, questionno, employeeno )
							Raw.update( )
						else:
							Raw.sql = "update sklcc_table set returnno = %d where serialno = '%s' and workno = %d and questionno = %d" % (
							count, serialno, workno, questionno )
							Raw.update( )
			sync_table_from_record( serialno )
			if get_record_totalreturn( serialno ) == 0:
				Raw.sql = "delete from sklcc_record where serialno = '%s'" % serialno
				Raw.update( )
		except Exception, e:
			make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )

		return HttpResponse( )
	else:
		return HttpResponse( )


def tables_check( request ):
	status = request.session['status']
	if 2 in status or 4 in status:
		username = request.session['username']
		em_number = request.session['employeeno']
		html = get_template( 'tables_check.html' )
		return TemplateResponse( request, html, locals( ) )
	else:
		return HttpResponseRedirect( '/warning/' )


def choose_check( request ):
	start = datetime.datetime.now( )
	status = request.session['status']
	if 4 in status:
		username = request.session['username']
		em_number = request.session['employeeno']
		employeename = request.session['employee']
		html = get_template( 'choose_check.html' )
		date = Current_time.get_now_date( )
		url = "/return_check_check/?start=%s&end=%s" % ( date, date )
		record_not_check_list = find_record_state_is( 0, username, 4, 1 )
		record_have_checked_list = find_record_state_is( 1, username, 4, 0 )
		return TemplateResponse( request, html,
		                         { 'username': username, 'em_number': em_number, 'employeename': employeename,
		                           'date': date, 'url': url, 'record_not_check_list': record_not_check_list,
		                           'record_have_checked_list': record_have_checked_list } )
	else:
		return HttpResponseRedirect( '/warning/' )


def pass_table( request ):
	serialno = request.GET['code']
	is_measure = request.GET['is_measure'] if 'is_measure' in request.GET else '0'
	update_all_state_to( serialno, 1, True if is_measure == '1' else False )
	Raw = Raw_sql( )
	T = Current_time( )
	if is_measure == '0':
		Raw.sql = "update sklcc_record set assessor = '%s', assessor_no = '%s',assesstime = '%s' where serialno = '%s'" % (
		request.session['employee'], request.session['employeeno'], T.time_str, serialno )
		Raw.update( )
	else:
		Raw.sql = "update sklcc_measure_record set assessor = '%s', assessor_no = '%s', assesstime = '%s' where serialno = '%s'" % (
		request.session['employee'], request.session['employeeno'], T.time_str, serialno )
		Raw.update( )
	return HttpResponse( )


def table_read_only( request ):
	status = request.session['status']
	if 5 in status or 3 or 2 or 4 or 15 in status:
		html = get_template( 'table_read_only.html' )
		return TemplateResponse( request, html )
	else:
		return HttpResponseRedirect( '/warning/' )


def table_measure( request ):
	Raw = Raw_sql( )
	serialno = request.GET['serialno']
	Raw.sql = "select distinct barcode from sklcc_measure_info where serialno = '%s'" % serialno
	target_list = Raw.query_all( )
	res = []
	if target_list != False:
		for target in target_list:
			temp = get_measure_info_by_barcode( target[0], request.session['employeeno'] )
			new_temp = { }
			new_temp['serialno'] = temp['serialno']
			new_temp['barcode'] = temp['barcode']
			#for k,v in
			res.append( get_measure_info_by_barcode( target[0], request.session['employeeno'] ) )
	Raw.sql = "select createtime, assesstime, inspector, inspector_no, size, styleno, batch, departmentno, measure_count from sklcc_measure_record where serialno = '%s'" % serialno
	info_list = Raw.query_one( )

	if info_list != False:
		createtime = info_list[0][0:10]
		departmentno = info_list[7]
		department = find_department_name( departmentno )
		measure_count = info_list[8]
		size = info_list[4]
		inspector = info_list[2]
		batch = info_list[6]
	html = get_template( 'table_measure.html' )
	return TemplateResponse( request, html, locals( ) )


def table_measure_read_only( request ):
	Raw = Raw_sql( )
	serialno = request.GET['serialno']
	is_check = int( request.GET['state'] ) if 'state' in request.GET else 0
	Raw.sql = "select distinct barcode from sklcc_measure_info where serialno = '%s'" % serialno

	target_list = Raw.query_all( )

	res = []
	if target_list != False:
		for target in target_list:
			temp = get_measure_info_by_barcode( target[0], request.session['employeeno'] )
			new_temp = { }
			new_temp['serialno'] = temp['serialno']
			new_temp['barcode'] = temp['barcode']
			#for k,v in
			res.append( get_measure_info_by_barcode( target[0], request.session['employeeno'] ) )
	Raw.sql = "select createtime, assesstime, inspector, inspector_no, size, styleno, batch, departmentno, measure_count from sklcc_measure_record where serialno = '%s'" % serialno
	info_list = Raw.query_one( )
	info_list = Raw.query_one( )

	if info_list != False:
		createtime = info_list[0][0:10]
		departmentno = info_list[7]
		measure_count = info_list[8]
		size = info_list[4]
		inspector = info_list[2]
		batch = info_list[6]
	html = get_template( 'table_measure_read_only.html' )
	return TemplateResponse( request, html, locals( ) )


def table_measure_data( request ):
	Raw = Raw_sql( )
	serialno = request.GET['serialno']
	Raw.sql = "select distinct barcode, styleno from sklcc_measure_info where serialno = '%s'" % serialno
	target_list = Raw.query_all( )

	res = []
	if target_list != False:
		for target in target_list:
			temp = get_measure_info_by_barcode( target[0], request.session['employeeno'] )
			new_temp = { }
			if temp != False:
				new_temp.clear( )
				new_temp['serialno'] = temp['serialno']
				new_temp['barcode'] = temp['barcode']
				new_temp['data'] = []
				for k, v in dict( temp ).items( ):
					if k not in ['barcode', 'serialno']:
						new_temp['data'].append(
							{ 'has_balance_error': 'true' if len( v[0] ) != 1 else 'false', 'partition_name': k,
							  'res': v, 'common_difference': get_common_difference( target[1], k ),
							  'symmetry': get_symmetry( target[1], k ), 'standard': get_measure_res( target[1], k ), } )

			res.append( new_temp )
	return HttpResponse( simplejson.dumps( res, ensure_ascii = False ) )


def partion_set( request ):
	em_number = request.session['employeeno']
	employeename = request.session['employee']
	Raw = Raw_sql( )
	html = get_template( 'partition_set.html' )
	Raw.sql = "select measure_type_id, measure_type_name from sklcc_measure_type "
	measure_type_list = []
	target_list = Raw.query_all( )
	if target_list != False:
		for i, one in enumerate( target_list ):
			temp = { 'id': one[0], 'type': one[1] }
			Raw.sql = "select partition from sklcc_measure_partition where measure_type_id = '%s'" % one[0]
			temp_list = Raw.query_all( )
			temp['partition_list'] = []
			if temp_list != False:
				for one in temp_list:
					temp['partition_list'].append( one[0] )
			temp['count'] = str( len( temp_list ) + 1 if temp_list != False else 1 )
			measure_type_list.append( temp )
	return TemplateResponse( request, html, locals( ) )


def submit_partion_set( request ):
	Raw = Raw_sql( )
	json = request.POST['json']
	result = simplejson.loads( json )
	id = result[0]['type_id'] if 'type_id' in result[0] else uuid.uuid1( )
	Raw.sql = "delete from sklcc_measure_type where measure_type_id = '%s'" % id
	Raw.update( )
	Raw.sql = "insert into sklcc_measure_type values( '%s', '%s' )" % ( id, result[0]['type_name'] )
	Raw.update( )

	for one in result[0]['partition_list']:
		Raw.sql = "insert into sklcc_measure_partition( measure_type_id, partition ) values( '%s', '%s' )" % ( id, one )
		Raw.update( )

	return HttpResponse( )


def delete_partion_set( request ):
	Raw = Raw_sql( )
	id = request.GET['id']
	Raw.sql = "delete from sklcc_measure_type where measure_type_id = '%s'" % id
	Raw.update( )

	return HttpResponse( )


#################################### *@*       end of choose and check        *@* ######################################
################################################*** first check ***#####################################################

def line_chart( request ):
	status = request.session['status']
	if 3 in status or 4 in status or 6 in status:
		username = request.session['username']
		em_number = request.session['employeeno']
		employeename = request.session['employee']
		html = get_template( 'line_chart.html' )
		Raw = Raw_sql( )
		Raw.sql = "select distinct StyleNO from ProduceMaster WITH (NOLOCK)"

		style_list = list( )
		for temp in Raw.query_all( 'MSZ' ):
			style_list.append( temp[0] )

		return TemplateResponse( request, html, locals( ) )
	else:
		return HttpResponseRedirect( '/warning/' )


def update_line_chart_dept( request ):
	style = request.GET['model']
	Raw = Raw_sql( )
	Raw.sql = "select distinct Department from ProduceMaster WITH (NOLOCK) where StyleNO = '%s'" % style
	target_list = Raw.query_all( 'MSZ' )

	json = []

	if target_list != False:
		for target in target_list:
			json.append( { 'department': target[0], } )
	return HttpResponse( simplejson.dumps( json, ensure_ascii = False ) )


def update_line_chart_batch( request ):
	style = request.GET['model']
	department = request.GET['dept']
	Raw = Raw_sql( )
	Raw.sql = "select Batch from ProduceMaster WITH (NOLOCK) where StyleNO = '%s' and Department = '%s'" % (
	style, department )
	target_list = Raw.query_all( 'MSZ' )
	json = []

	if target_list != False:
		for target in target_list:
			json.append( { 'batch': target[0].decode( 'gbk' ) } )

	return HttpResponse( simplejson.dumps( json, ensure_ascii = False ) )


def update_line_chart( request ):
	"""@type:1
		疵点计数
		@type:2
		返修率
	"""
	try:
		type = request.GET['type']
		batch_list = request.GET.getlist( 'batch' )
		start = request.GET['start']
		end = request.GET['end']
		if type == "1":
			json = []
			Raw = Raw_sql( )

			for batch in batch_list:
				distance = get_time_distance_list( start, end )
				temp = []

				for day in distance:
					Raw.sql = r"select totalreturn from sklcc_record where batch = '%s' and left( createtime, 10 ) = '%s'" % (
					batch, day )
					target_list = Raw.query_all( )
					if target_list == False:
						temp.append( 0 )
					else:
						totalreturn = 0
						for target in target_list:
							totalreturn += target[0]
						temp.append( totalreturn )
				json.append( temp )
		else:
			json = []
			Raw = Raw_sql( )

			for batch in batch_list:
				start_p = time_form( start )
				end_p = time_form( end )
				temp = []
				for i in range( (end_p - start_p).days ):
					start_p = start_p + datetime.timedelta( days = 1 )
					Raw.sql = "select totalreturn, totalnumber from sklcc_record where batch = '%s' and left( createtime, 10 ) = '%s'" % (
					batch, start_p.date( ) )
					target_list = Raw.query_all( )
					if target_list == False:
						temp.append( 0 )
					else:
						totalreturn = 0
						totalnumber = 0
						for target in target_list:
							totalreturn += target[0]
							totalnumber += target[1]
						temp.append( int( float( totalreturn ) / float( totalnumber ) * 100 ) )
				json.append( temp )
		return HttpResponse( simplejson.dumps( json, ensure_ascii = False ) )
	except Exception, e:
		make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )


################################################*** second check ***#####################################################
################################# *@*       start of recheck_dataentry        *@* ######################################
def recheck( request ):
	status = request.session['status']
	if 1 in status:
		em_number = request.session['employeeno']
		username = request.session['username']
		html = get_template( 'recheck.html' )
		employeename = request.session['employee']
		T = Current_time( )
		date = T.get_date( )

		Raw = Raw_sql( )
		Raw.sql = "select departmentno from sklcc_employee_authority where username = '%s' and authorityid = 1" % username
		target_list = Raw.query_all( )
		department_list = list( )
		for target in target_list:
			department = find_department_name( target[0] )
			department_list.append( department )
		employee_list = []
		Raw.sql = "select distinct username from sklcc_employee_authority where authorityid = 0"
		target_list = Raw.query_all( )

		if target_list != False:
			for target in target_list:
				username_t = target[0]
				employee_t = Employee( )
				employee_t.employeeno = find_employeeno( username_t )
				employee_t.employee = find_em_name( employee_t.employeeno )
				employee_list.append( employee_t )

		Raw.sql = "select QuestionCode, isStrong, isBad, QuestionNo from QCQuestion WITH (NOLOCK) where isStrong = 1 order by QuestionNo "
		QCQ = Raw.query_all( 'MSZ' )
		question_list = []
		for one in QCQ:
			question = Question( )
			question.questionname = one[0].decode( 'gbk' )
			question.questionno = one[3]
			question.questiontype = get_question_type( one[3] )
			question_list.append( question )
		Raw.sql = "select QuestionCode, isStrong, isBad, QuestionNo from QCQuestion WITH (NOLOCK) where isStrong != 1 order by QuestionNo "
		QCQ = Raw.query_all( 'MSZ' )
		for one in QCQ:
			question = Question( )
			question.questionname = one[0].decode( 'gbk' )
			question.questionno = one[3]
			question.questiontype = get_question_type( one[3] )
			question_list.append( question )

		Raw.sql = "select totalnumber, employeeno, employee, questionname, questionno, returnno from sklcc_recheck_bald where left( createtime,10 ) = '%s' and recheckor_no = '%s'" % (
		date, em_number )
		target_list = Raw.query_all( )

		bald_list = []

		if target_list != False:
			for target in target_list:
				if target[5] == 0:
					continue
				bald = Bald_info( )
				bald.employee = target[2]
				bald.employeeno = target[1]
				bald.questionname = target[3]
				bald.questionno = target[4]
				bald.returnno = target[5]
				bald_list.append( bald )

			totalnumber = target_list[0][0]
		else:
			totalnumber = ''

		return TemplateResponse( request, html,
		                         { "employeename": employeename, "em_number": em_number, 'username': username,
		                           'department_list': department_list, 'employee_list': employee_list,
		                           'question_list': question_list, 'totalnumber': totalnumber,
		                           'bald_list': bald_list }, )
	else:
		return HttpResponseRedirect( '/warning/' )


def get_size_by_batch( batch ):
	Raw = Raw_sql( )
	Raw.sql = "select distinct size from sklcc_style_measure where styleno = '%s'" % ( batch.split( '-' )[0] )
	target_list = Raw.query_all( )
	size_list = []
	if target_list != False:
		for target in target_list:
			size_list.append( target[0] )

	return size_list


def flush_buttons_recheck( request ):
	try:
		inspector_no = request.session['employeeno']
		batch        = request.GET['batch']
		contentid    = request.GET['contentid'] if 'contentid' in request.GET else False
		print contentid
		Raw          = Raw_sql( )
		Raw.sql      = "select QuestionCode, isStrong, isBad, QuestionNO from QCQuestion WITH (NOLOCK) order by QuestionNO"
		#distinguish question type:| 0,weak | 1,bad | 2,strong |
		QCQ = Raw.query_all( 'MSZ' )
		xml = "<xml>"
		xml += "<QC>"
		for i in range( len( QCQ ) ):
			question = QCQ[i]
			if question[1]:
				xml += """<QCQuestion code = "%s" class="2" no = "%d" />""" % (
				question[0].decode( 'gbk' ), question[3] )
			elif question[2]:
				xml += """<QCQuestion code = "%s" class="1" no = "%d" />""" % (
				question[0].decode( 'gbk' ), question[3] )
			else:
				xml += """<QCQuestion code = "%s" class="0" no = "%d" />""" % (
				question[0].decode( 'gbk' ), question[3] )
		xml += "</QC>"

		###find workline
		Raw.sql = "select ProduceMasterID from ProduceMaster WITH (NOLOCK) where batch = '%s'" % batch
		target = Raw.query_one( 'MSZ' )
		ProduceMasterID = target[0]
		Raw.sql = "select WorkLineNo, WorkName from ProduceStyle WITH (NOLOCK) where ProduceMasterID = '%s' order by WorkLineNo" % ProduceMasterID
		program_list = Raw.query_all( 'MSZ' )
		if program_list != False:
			xml += "<PR>"
			#print raw[1]
			for program in program_list:
				workno = program[0]
				workname = program[1]
				if workname == None or workno == None:
					continue
				xml += """<ProduceStyle WorkLineNo = '%d' WorkName = "%s" />""" % ( workno, workname.decode( 'gbk' ) )

			xml += """<ProduceStyle WorkLineNo = "100" WorkName = "裁剪" Employee = "裁剪组" />""".decode( 'utf-8' )
			xml += """<ProduceStyle WorkLineNo = "101" WorkName = "整烫" Employee = "整烫组" />""".decode( 'utf-8' )
			xml += """<ProduceStyle WorkLineNo = "0" WorkName = "未知" Employee = "未知" />""".decode( 'utf-8' )
		xml += "</PR>"
		if contentid != False:
			Raw.sql = "select workno, workname, questionname, questionno, returnno from sklcc_recheck_content where" \
			          " contentid = '%s'" % contentid
			RC_list = Raw.query_all( )
			if RC_list != False:
				xml += "<RC>"
				for RC in RC_list:
					xml += """<record Workno = "%s" Work = "%s" QCno = "%s" QC = "%s" no = "%d"/>""" % (
					RC[0], RC[1], RC[3], RC[2], RC[4] )
				xml += "</RC>"

			#为复用一检的函数使用的一检的函数
			res = get_measure_info_by_barcode( contentid, inspector_no )
			if res != False:
				xml += """<MERC>"""
				for k, v in dict( res ).items( ):
					if k != 'serialno' and k != 'barcode':
						xml += """<Merecord partition = "%s"> """ % k
						for t in v:
							if len( t ) == 2:
								xml += """<data value = "%f,%f" />""" % ( t[0], t[1] )
							else:
								xml += """<data value = "%f" />""" % t[0]
						xml += """</Merecord>"""
				xml += """</MERC>"""

			Raw.sql = "select TOP 1 samplenumber, totalnumber, inspector_no from sklcc_recheck_content a join sklcc_recheck_info b on a.serialno = b.serialno where contentid = '%s'" % contentid
			target = Raw.query_one( )
			samplenumber = 0
			totalnumber  = 0
			inspector_no = ""
			inspector    = ""
			if target != False:
				samplenumber = target[0]
				totalnumber = target[1]
				inspector_no = target[2]
				inspector = find_em_name( inspector_no )
			xml += """<IF>"""
			xml += """<info sample = "%d" total = "%d" employeeno = "%s" employee = "%s" />""" % (
			samplenumber, totalnumber, inspector_no, inspector )
			xml += """</IF>"""
		size_list = get_size_by_batch( batch )
		if len( size_list ) != 0:
			xml += """<SZ>"""
			xml += """<size size_list = """
			xml += '"'
			for size in size_list:
				xml += size + ';'
			xml = xml[:-1] + '"' + "/>"
			xml += """</SZ>"""

		xml += "</xml>"
		return HttpResponse( xml )
	except Exception, e:
		make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )


def recheck_update_batch_and_inspector( request ):
	#reload(sys)
	#sys.setdefaultencoding('utf-8')
	department = request.GET['department']
	departmentno = find_department_no( department )
	Raw = Raw_sql( )
	json = dict( )
	json1 = list( )
	departmentno_list = []
	all_department_list = get_all_department( )
	for department_t in all_department_list:
		departmentno_list.append( department_t.departmentno )
	shop1 = []
	shop2 = []
	shop3 = []
	choose_list = []
	Raw.sql = "select distinct username, departmentno from sklcc_employee_authority where authorityid = 0"
	target_list = Raw.query_all( )
	if target_list != False:
		for one in target_list:
			if str( one[1] ) == departmentno:
				choose_list.append( one[0] )
			elif str( one[1] ) in DEPT_SHOP1:
				shop1.append( one[0] )
			elif str( one[1] ) in DEPT_SHOP2:
				shop2.append( one[0] )
			elif str( one[1] ) in DEPT_SHOP3:
				shop3.append( one[0] )
	username_list = choose_list + shop1 + shop2 + shop3
	distinctUsername = list( set( username_list ) )
	distinctUsername.sort( key = username_list.index )
	for username in distinctUsername:
		employeeno = find_employeeno( username )
		if employeeno == '0000':
			continue
		json1.append(
			{ 'inspector_no': copy.deepcopy( employeeno ), 'inspector': copy.deepcopy( find_em_name( employeeno ) ), } )
	month_distance = int( request.GET['month'] )
	T = Current_time( )
	now_year = int( T.get_date( ).split( '-' )[0] )
	now_month = int( T.get_date( ).split( '-' )[1] )
	month_list = []
	month_list.append( now_month )
	for i in range( 1, month_distance ):
		if ( ( now_month - i ) + 12 ) % 12 == 0:
			month_list.append( 12 )
		else:
			month_list.append( ( ( now_month - i ) + 12 ) % 12 )
	#生成时间列表逐个月份从PM表过滤
	month_list.reverse( )
	target_list = []
	for month in month_list:
		if month > now_month:
			#时间已经跨越到前一年
			timestr = str( now_year - 1 ) + '-' + str( month ).rjust( 2, '0' )
		else:
			timestr = str( now_year ) + '-' + str( month ).rjust( 2, '0' )
		#rjust 左填充不够补0
		if request.GET['is_clear'] == 'true':
			#convert函数最后一个参数是字符串的格式号
			Raw.sql = u"select batch from ProduceMaster WITH (NOLOCK) where DepartmentNo = '%s' and ( FormState = '" % departmentno + u"清款" + "' or FormState = '" + u"审核" + "' ) and left( convert( varchar(100),FormDate, 21 ), 7 ) = '%s' " % (
			timestr )
			temp = Raw.query_all( 'MSZ' )
			if temp != False:
				target_list += Raw.query_all( 'MSZ' )
		else:
			#为了减少刷新出的批次号，从一检检验表中查询一检检过的批次
			#Raw.sql = "select batch from ProduceMaster where DepartmentNo = '%s' and FormState = '审核' and left( convert( varchar(100), FormDate , 21 ), 7 ) = '%s'".decode('utf-8')% ( departmentno, timestr )
			#temp    = Raw.query_all( 'MSZ' )
			Raw.sql = "select distinct batch from sklcc_record where departmentno = '%s' and left( createtime, 7 ) = '%s'" % (
			departmentno, timestr )
			temp = Raw.query_all( )
			if temp != False:
				target_list += Raw.query_all( )
			#target_list += Raw.query_all( 'MSZ' )
	if target_list != False:
		target_list = list( set( target_list ) )
	json2 = list( )

	if target_list != False:
		for target in target_list:
			try:
				json2.append( { 'batch': unicode( target[0] ) } )
			except Exception:
				json2.append( { 'batch': target[0].decode( 'gbk' ) } )
	json['inspector'] = json1
	json['batch'] = json2

	return HttpResponse( simplejson.dumps( json, ensure_ascii = False ) )


def find_department_no( department ):
	Raw = Raw_sql( )
	Raw.sql = "select departmentno from sklcc_department where department = '%s'" % department
	target = Raw.query_one( )
	return target[0]


def commit_res_recheck( request ):
	try:
		xml = request.POST['xml']
		Raw = Raw_sql( )
		reload( sys )
		sys.setdefaultencoding( 'utf-8' )
		root = ElementTree.fromstring( xml )
		id = root.getiterator( 'id' )[0].text
		department = root.getiterator( 'group' )[0].text
		departmentno = find_department_no( department )
		T = Current_time( )
		date = T.time_str
		batch = root.getiterator( 'no' )[0].text
		state = 2
		is_recheck = True if root.getiterator( 'is_recheck' )[0].text == 'true' else False
		inspector_no = root.getiterator( 'inspector_no' )[0].text
		inspector = find_em_name( inspector_no )
		recheckor_no = request.session['employeeno']
		recheckor = request.session['employee']
		totalnumber = root.getiterator( 'totalnumber' )[0].text
		sample = root.getiterator( 'sample' )[0].text
		ok = root.getiterator( 'conclusion' )[0].text
		try:
			size = root.getiterator( 'size' )[0].text
		except Exception:
			size = None
		leader_no = ""
		leader = ""
		assesstime = ""

		Raw.sql = "select serialno from sklcc_recheck_content where contentid = '%s'" % id
		target = Raw.query_one( )
		if target != False:
			serialno = target[0]
		else:
			Raw.sql = "select serialno from sklcc_recheck_info where left( createtime, 10 ) = '%s' and batch = '%s' and state = " \
			          "2 and inspector_no = '%s' and recheckor_no = '%s'" % (
			          T.get_date( ), batch, inspector_no, recheckor_no )
			res = Raw.query_one( )
			serialno = res[0] if res != False else uuid.uuid1( )

		record_list = root.getiterator( 're' )
		Raw.sql = "delete from sklcc_recheck_content where contentid = '%s'" % id
		Raw.update( )
		if len( record_list ) == 0:
			recheckinfo = dict( ok = ok, state = state, departmentno = departmentno, department = department,
			                    leader = leader, leader_no = leader_no, inspector = inspector,
			                    inspector_no = inspector_no, recheckor_no = recheckor_no, recheckor = recheckor,
			                    batch = batch, assesstime = assesstime, id = id, date = date, serialno = serialno,
			                    totalnumber = int( totalnumber ), sample = int( sample ), workno = 0, workname = "",
			                    questionname = "", questionno = 0, returnno = 0, is_recheck = is_recheck )

			written_into_recheck( recheckinfo )
		else:
			for record in record_list:
				workno = record.attrib['program_no']
				workname = record.attrib['program_name']
				returnno = record.attrib['count']
				questionno = record.attrib['mistake_no']
				questionname = record.attrib['mistake_name']
				recheckinfo = dict( ok = ok, state = state, departmentno = departmentno, department = department,
				                    leader = leader, leader_no = leader_no, inspector = inspector,
				                    inspector_no = inspector_no, recheckor_no = recheckor_no, recheckor = recheckor,
				                    batch = batch, assesstime = assesstime, id = id, date = date, serialno = serialno,
				                    totalnumber = int( totalnumber ), sample = int( sample ), workno = int( workno ),
				                    workname = workname, questionname = questionname, questionno = int( questionno ),
				                    returnno = int( returnno ), is_recheck = is_recheck )
				written_into_recheck( recheckinfo )

		if request.POST['json'] != '[]':
			measure_json = simplejson.loads( request.POST['json'] )
			today = date[0:10]
			Raw.sql = "select serialno from sklcc_measure_info a join sklcc_measure_record b on a.serialno = b.serialno" \
			          " where barcode = '%s' and inspector_no = '%s'" % (id, recheckor_no)
			target = Raw.query_one( )
			if target != False:
				serialno = target[0]
			else:
				Raw.sql = "select serialno from sklcc_measure_record where batch = '%s' and state = 2 and " \
				          "departmentno = '%s' and inspector_no = '%s' and size = '%s' and is_first_check = 0 and left( createtime, 10 ) = '%s'" % (
				          batch, departmentno, recheckor_no, size, today )
				target = Raw.query_one( )
				serialno = uuid.uuid1( ) if target == False else target[0]
			insert_list = prase_measure_json( id, serialno, batch.split( '-' )[0], departmentno, size, recheckor_no,
			                                  batch, measure_json )
			insert_res = { }

			#first delete sklcc_measure_info and sklcc_measure_record
			Raw.sql = "delete sklcc_measure_info from sklcc_measure_info a join sklcc_measure_record b on a.serialno = b.serialno where" \
			          " barcode = '%s' and inspector_no = '%s' and state = 2" % ( id, recheckor_no )
			Raw.update( )
			Raw.sql = "select TOP 1 * from sklcc_measure_info where serialno = '%s'" % serialno
			target = Raw.query_one( )
			if target == False:
				Raw.sql = "delete from sklcc_measure_record where serialno = '%s'" % serialno
				Raw.update( )
			else:
				Raw.sql = "select sum( count_i )  from(  select max( count_id ) count_i from sklcc_measure_info where " \
				          "serialno = '%s' group by barcode ) a" % serialno
				measure_count = Raw.query_one( )[0]
				Raw.sql = "update sklcc_measure_record set measure_count = %d where serialno = '%s'" % (
				measure_count, serialno )
				Raw.update( )

			for insert in insert_list:
				insert_res = written_into_measure_info( insert )
			written_into_measure_record( insert_res, 'False' )

		temp = temp_Info( )
		temp.serialno = serialno
		temp.inspector = recheckor
		temp.inspector_no = recheckor_no
		written_return_check_in_datebase( temp, 2 )
		return HttpResponse( )
	except Exception, e:
		make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )


def commit_bald_recheck( request ):
	info = request.POST['json']
	json = simplejson.loads( info )
	totalnumber = int( json['count'][0] )
	Raw = Raw_sql( )
	T = Current_time( )
	date = T.get_date( )
	createtime = T.time_str
	recheckor_no = request.session['employeeno']
	recheckor = request.session['employee']

	Raw.sql = "delete from sklcc_recheck_bald where recheckor_no = '%s' and left( createtime, 10 ) = '%s'" % (
	recheckor_no, date )
	Raw.update( )

	if len( json['record'] ) != 0:
		record_get_list = json['record']
		for record in record_get_list:
			Raw.sql = "insert into sklcc_recheck_bald( createtime, employeeno, employee, totalnumber, questionname, questionno, returnno, recheckor, recheckor_no )" \
			          " values( '%s', '%s', '%s', %d, '%s', %d, %d, '%s', '%s')" % (
			          createtime, record['employeeno'], record['employeename'], totalnumber, record['mistakename'],
			          int( record['mistakeno'] ), int( record['count'] ), recheckor, recheckor_no )
			Raw.update( )
	else:
		Raw.sql = "insert into sklcc_recheck_bald( createtime, employeeno, employee, totalnumber, questionname, questionno, returnno, recheckor, recheckor_no )" \
		          " values( '%s', '%s', '%s', %d, '%s', %d, %d, '%s', '%s')" % (
		          createtime, '', '', totalnumber, '', 0, 0, recheckor, recheckor_no )
		Raw.update( )
	return HttpResponse( )


def written_into_recheck( recheckinfo ):
	Raw = Raw_sql( )

	Raw.sql = "insert into sklcc_recheck_content values( '%s', '%s', '%s', %d, %d, %d, '%s', '%s', %d, %d, '%s'," % (
	recheckinfo['id'], recheckinfo['date'], recheckinfo['serialno'], int( recheckinfo['totalnumber'] ),
	int( recheckinfo['sample'] ), int( recheckinfo['workno'] ), recheckinfo['workname'], recheckinfo['questionname'],
	int( recheckinfo['questionno'] ), int( recheckinfo['returnno'] ), str( recheckinfo['ok'] ) )
	if recheckinfo['is_recheck']:
		Raw.sql += "'True' )"
	else:
		Raw.sql += "'False' )"
	Raw.update( )
	Raw.sql = "select * from sklcc_recheck_info where serialno = '%s'" % recheckinfo['serialno']
	target = Raw.query_one( )

	if target == False:
		Raw.sql = "insert into sklcc_recheck_info values( %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % (
		recheckinfo['state'], recheckinfo['serialno'], recheckinfo['date'], recheckinfo['departmentno'],
		recheckinfo['department'], recheckinfo['inspector'], recheckinfo['inspector_no'], recheckinfo['recheckor'],
		recheckinfo['recheckor_no'], recheckinfo['leader'], recheckinfo['leader_no'], recheckinfo['batch'], '' )
		Raw.update( )


################################## *@*       end of recheck_dataentry        *@* #######################################

######################### *@*      start of recheck_choose and recheck_check     *@* ###################################

def choose_recheck( request ):
	status = request.session['status']
	if 3 in status:
		em_number = request.session['employeeno']
		username = request.session['username']
		status = request.session['status']
		html = get_template( 'choose_recheck.html' )
		employeename = request.session['employee']
		record_have_committed_list = find_recheck_info( 0, username, 3 )
		record_have_committed_list += find_recheck_info( 1, username, 3 )
		record_not_commit_list = find_recheck_info( 2, username, 3 )
		T = Current_time( )
		date = T.get_date( )
		url = "/recheck_return_check/?start=%s&end=%s" % ( date, date )
		return TemplateResponse( request, html, locals( ) )
	else:
		return HttpResponseRedirect( '/warning/' )


def find_recheck_info_help_function( Raw_Sql, authorityid_in_use ):
	Raw = Raw_sql( )
	Raw.sql = Raw_Sql
	target_list = Raw.query_all( )
	record_list = list( )
	record = Record_info( )
	if target_list != False:
		for target in target_list:
			record.check_type = ""
			state = target[0]
			serialno = target[2]
			departmentno = target[3]
			department = target[4]
			inspector = target[5]
			inspector_no = target[6]
			recheckor = target[7]
			batch = target[9]
			createtime = target[1]

			string = str( createtime ).split( ' ' )[0].split( '-' )
			year = int( string[0] )
			month = int( string[1] )
			day = int( string[2] )
			createtime_form = datetime.datetime( year, month, day )
			Raw.sql = "select days from sklcc_config"
			target = Raw.query_one( )

			if (datetime.datetime.today( ) - createtime_form).days > target[0]:
				continue

			record.state = state
			record.batch = batch
			record.createtime = createtime.split( '.' )[0][5:-3]
			record.departmentno = departmentno
			record.department = department
			record.serialno = serialno
			record.inspector = inspector
			record.totalnumber = 0
			record.totalreturn = 0
			record.bad = 0
			record.strong = 0
			record.weak = 0
			record.batchnumber = 0
			#normal_check 0 partition_measure 1
			record.check_id = 0
			Raw = Raw_sql( )
			Raw.sql = "select samplenumber, returnno, questionno from sklcc_recheck_content where serialno = '%s'" % serialno
			is_serialno_list = Raw.query_all( )

			if is_serialno_list == False:
				if state == 2:
					record.url = '/recheck_table?%d#%s' % (state, serialno)
				elif state == 0 and authorityid_in_use == 5:
					record.url = '/recheck_check_table?%d#%s' % (state, serialno)
				else:
					record.url = '/recheck_read_only_table?%d#%s' % (state, serialno)
				record_list.append( copy.deepcopy( record ) )
				continue

			for one in is_serialno_list:
				record.totalreturn += one[1]
				if get_question_type( one[2] ) == 2:
					record.strong += 1
				elif get_question_type( one[2] ) == 1:
					record.bad += 1
				elif get_question_type( one[2] ) == None:
					pass
				else:
					record.weak += 1
			Raw.sql = "select distinct contentid, samplenumber, totalnumber, is_recheck from sklcc_recheck_content where serialno = '%s'" % serialno
			target_list = Raw.query_all( )

			if target_list != False:
				for target in target_list:
					record.totalnumber += target[1]
					if target[3] == 1:
						#normal_check 0 partition_measure 1
						record.check_type = "(含复检)"
						continue
					record.batchnumber += target[2]
			if state == 2:
				record.url = '/recheck_table?%d#%s' % (state, serialno)
			elif state == 0 and authorityid_in_use == 5:
				record.url = '/recheck_check_table?%d#%s' % (state, serialno)
			else:
				record.url = '/recheck_read_only_table?%d#%s' % (state, serialno)
			record_list.append( copy.deepcopy( record ) )

	return record_list


def find_recheck_info( state, username, authorityid_in_use ):
	Raw = Raw_sql( )
	employeeno = find_employeeno( username )
	departmentno_list = find_department_authority_user( username, authorityid_in_use )
	if authorityid_in_use == 3:
		record_list = []
		for departmentno in departmentno_list:
			SQL = "select state,createtime,serialno,departmentno,department,inspector,inspector_no,recheckor,recheckor_no, batch from sklcc_recheck_info where state = %d and recheckor_no = '%s' and departmentno = '%s'" % (
			state, employeeno, departmentno )
			record_list += find_recheck_info_help_function( SQL, authorityid_in_use )
		Raw.sql = "select serialno, createtime, inspector, inspector_no, state, assessor, assessor_no, assesstime, departmentno," \
		          "batch, size, measure_count from sklcc_measure_record where is_first_check = 0 and state = %d and inspector_no = '%s' order by createtime desc" % (
		          state, employeeno )
		record_list += find_measure_record_state_is_help_function( Raw.sql, state, False )

		return record_list
	else:
		record_list = []
		for departmentno in departmentno_list:
			SQL = "select state,createtime,serialno,departmentno,department,inspector,inspector_no,recheckor,recheckor_no, batch from sklcc_recheck_info where state = %d and departmentno = '%s'" % (
			state, departmentno )
			record_list += find_recheck_info_help_function( SQL, authorityid_in_use )
			Raw.sql = "select serialno, createtime, inspector, inspector_no, state, assessor, assessor_no, assesstime, departmentno," \
			          "batch, size, measure_count from sklcc_measure_record where state = %d and departmentno = '%s' and is_first_check = 0 order by createtime desc" % (
			          state, departmentno )
			record_list += find_measure_record_state_is_help_function( Raw.sql, state, False )
		return record_list


def delete_recheck_table( request ):
	serialno = request.GET['serialno']

	Raw = Raw_sql( )
	Raw.sql = "delete from sklcc_recheck_content where serialno = '%s'" % serialno
	Raw.update( )

	Raw.sql = "delete from sklcc_recheck_info where serialno = '%s'" % serialno
	Raw.update( )

	Raw.sql = "delete from sklcc_return_check where serialno = '%s'" % serialno
	Raw.update( )
	return HttpResponse( 1 )


def delete_recheck_content( request ):
	Raw = Raw_sql( )
	contentid = request.GET['content_id']
	serialno = request.GET['serialno']
	Raw.sql = "delete from sklcc_recheck_content where contentid = '%s'" % contentid
	Raw.update( )

	Raw.sql = "select * from sklcc_recheck_content where serialno = '%s'" % serialno
	if Raw.query_all( ) == False:
		Raw.sql = "delete from sklcc_recheck_info where serialno = '%s'" % serialno
		Raw.update( )
	return HttpResponse( 1 )


def recheck_table( request ):
	html = get_template( 'tables_recheck.html' )
	return TemplateResponse( request, html )


def recheck_read_only_table( request ):
	html = get_template( 'tables_recheck_read_only.html' )
	return TemplateResponse( request, html )


def recheck_check_table( request ):
	html = get_template( 'tables_recheck_check.html' )
	return TemplateResponse( request, html )


def syncdb_table_content_and_info( serialno ):
	Raw = Raw_sql( )
	Raw.sql = "select * from sklcc_recheck_content where serialno = '%s'" % serialno
	target_list = Raw.query_all( )
	if target_list == False:
		Raw.sql = "delete from sklcc_recheck_info where serialno = '%s'" % serialno
		Raw.update( )


def save_recheck_change( xml, serialno ):
	"""@count = 0
		<1>can not find in table recheck_content, do nothing.
		<2>can find in table recheck_content,  then delete it.
		@count != 0 && id, workno, question
		<1>can not find in table recheck_content, add it.
		<2>can find in table recheck_content, then fix it.
	"""
	reload( sys )
	sys.setdefaultencoding( 'utf-8' )
	root = ElementTree.fromstring( xml )
	rc_list = root.getiterator( 'rc' )
	Raw = Raw_sql( )
	for rc in rc_list:
		id = rc.attrib['id']
		count = int( rc.attrib['count'] )
		workno = int( rc.attrib['program'] )
		questionno = int( rc.attrib['mistake'] )
		workname = find_workname_in_sklcc_recheck_content( serialno, workno )

		questionname = find_questionname( questionno )
		createtime = str( datetime.date.today( ) )
		Raw.sql = "select serialno from sklcc_recheck_content where contentid = '%s' and workno = %d and questionno = %d" % (
		id, workno, questionno )
		target = Raw.query_one( )
		if target != False:
			if count == 0:
				serialno = target[0]
				Raw.sql = "delete from sklcc_recheck_content where contentid = '%s'" % id
				Raw.update( )
				syncdb_table_content_and_info( serialno )
			else:
				Raw.sql = "update sklcc_recheck_content set returnno = %d where contentid = '%s' and workno = %d and questionno = %d" % (
				count, id, workno, questionno )
				Raw.update( )
		else:
			if count != 0:
				Raw.sql = "select totalnumber, samplenumber from sklcc_recheck_content where contentid = '%s'" % id
				target = Raw.query_one( )
				totalnumber = target[0]
				samplenumber = target[1]
				serialno = str( serialno )
				workname = str( workname )
				questionname = questionname.decode( 'gbk' )
				Raw.sql = "insert into sklcc_recheck_content values( '%s', '%s', '%s', %d, %d, %d, '%s', '%s', %d, %d, 'False' )" % (
				id, createtime, serialno, totalnumber, samplenumber, workno, workname, questionname, questionno, count )
				Raw.update( )


def save_recheck_table( request ):
	try:
		xml = request.POST['xml']
		Raw = Raw_sql( )

		root = ElementTree.fromstring( xml )

		result_list = root.getiterator( 'result' )

		contentid = result_list[0].attrib['id']
		Raw.sql = "select serialno from sklcc_recheck_content where contentid = '%s'" % contentid
		target = Raw.query_one( )
		serialno = target[0]
		for result in result_list:
			contentid = result.attrib['id']
			ok = result.attrib['state']

			if ok == '1':
				Raw.sql = "update sklcc_recheck_content set ok = 'True' where contentid = '%s'" % contentid
			else:
				Raw.sql = "update sklcc_recheck_content set ok = 'False' where contentid = '%s'" % contentid
			Raw.update( )

		if root.find( 'rc' ) != None:
			save_recheck_change( xml, serialno )

		return HttpResponse( )
	except Exception, e:
		make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )


def update_recheck_info( request ):
	serialno = request.GET['code']
	xml = update_recheck_info_xml( serialno )
	return HttpResponse( xml )


def update_recheck_info_xml( serialno ):
	reload( sys )
	sys.setdefaultencoding( 'utf-8' )
	Raw = Raw_sql( )
	xml = """"""

	Raw.sql = "select distinct contentid from sklcc_recheck_content where serialno = '%s'" % serialno

	target_list = Raw.query_all( )

	id_list = list( )
	for target in target_list:
		id_list.append( target[0] )

	Raw.sql = "select department, inspector, inspector_no, batch, createtime from sklcc_recheck_info where serialno = '%s'" % serialno

	target = Raw.query_all( )[0]
	department = target[0]
	inspector = target[1]
	inspector_no = target[2]
	batch = target[3]
	date = target[4][0:-7]

	xml += """<xml>"""
	xml += """<group>"""
	xml += department
	xml += """</group>"""
	xml += """<inspector>"""
	xml += inspector
	xml += """</inspector>"""
	xml += """<inspectorno>"""
	xml += inspector_no
	xml += """</inspectorno>"""
	xml += """<no>"""
	xml += batch
	xml += """</no>"""
	xml += """<date>"""
	xml += date
	xml += """</date>"""

	for id in id_list:
		Raw.sql = "select distinct workno, workname, totalnumber, samplenumber, ok, is_recheck from sklcc_recheck_content where contentid = '%s'" % id
		workno_list = Raw.query_all( )
		if workno_list[0][4] == True:
			if workno_list[0][5] == 1:
				xml += """<record id = '%s' total = '%d' sample = '%d(含复检)' state = '1'>""" % (
				id, workno_list[0][2], workno_list[0][3] )
			else:
				xml += """<record id = '%s' total = '%d' sample = '%d' state = '1'>""" % (
				id, workno_list[0][2], workno_list[0][3] )
		else:
			if workno_list[0][5] == 1:
				xml += """<record id = '%s' total = '%d' sample = '%d(含复检)' state = '0'>""" % (
				id, workno_list[0][2], workno_list[0][3] )
			else:
				xml += """<record id = '%s' total = '%d' sample = '%d' state = '0'>""" % (
				id, workno_list[0][2], workno_list[0][3] )
		for workno in workno_list:
			xml += """<program name='%s' no='%s'>""" % ( workno[1], workno[0] )
			Raw.sql = "select questionno, questionname, returnno from sklcc_recheck_content where contentid = '%s' and workno = %d" % (
			id, workno[0] )
			target_list = Raw.query_all( )
			for target in target_list:
				if get_question_type( target[0] ) == None:
					xml += """<mistake0 name='%s' no='%d' count='%d'/>""" % (  target[1], target[0], target[2] )
				else:
					xml += """<mistake%d name='%s' no='%d' count='%d'/>""" % (
					get_question_type( target[0] ), target[1], target[0], target[2] )
			xml += """</program>"""
		xml += """</record>"""
	xml += """</xml>"""
	return xml


def update_recheck_state( request ):
	xml = request.POST['xml']
	root = ElementTree.fromstring( xml )
	result_list = root.getiterator( 'result' )

	Raw = Raw_sql( )
	contentid = result_list[0].attrib['id']
	Raw.sql = "select serialno from sklcc_recheck_content where contentid = '%s'" % contentid
	target = Raw.query_one( )
	serialno = target[0]
	for result in result_list:
		contentid = result.attrib['id']
		ok = result.attrib['state']
		if ok == '1':
			Raw.sql = "update sklcc_recheck_content set ok = 'True' where contentid = '%s'" % contentid
		else:
			Raw.sql = "update sklcc_recheck_content set ok = 'False' where contentid = '%s'" % contentid
		Raw.update( )

	Raw.sql = "select serialno from sklcc_recheck_content where contentid = '%s'" % contentid
	target = Raw.query_one( )
	serialno = target[0]

	if root.find( 'rc' ) != None:
		save_recheck_change( xml, serialno )

	Raw.sql = "select * from sklcc_recheck_info where serialno = '%s'" % serialno
	target = Raw.query_one( )
	if target != False:
		Raw.sql = "update sklcc_recheck_info set state = 0 where serialno = '%s'" % serialno
		Raw.update( )
	return HttpResponse( )


def choose_check_recheck( request ):
	status = request.session['status']
	if 5 in status:
		html = get_template( 'choose_recheck_check.html' )
		em_number = request.session['employeeno']
		username = request.session['username']
		employeename = request.session['employee']
		Raw = Raw_sql( )
		T = Current_time( )
		date = T.get_date( )
		record_not_commit_list = list( )
		record_have_committed_list = list( )
		url = "/recheck_return_check_check/?start=%s&end=%s" % ( date, date )
		record_not_commit_list += find_recheck_info( 0, username, 5 )
		record_have_committed_list += find_recheck_info( 1, username, 5 )

		return TemplateResponse( request, html, locals( ) )
	else:
		return HttpResponseRedirect( '/warning/' )


def pass_gather_recheck_table( request ):
	xml = request.POST['xml']
	root = ElementTree.fromstring( xml )
	result_list = root.getiterator( 'result' )

	Raw = Raw_sql( )
	contentid = result_list[0].attrib['id']
	Raw.sql = "select serialno from sklcc_recheck_content where contentid = '%s'" % contentid
	target = Raw.query_one( )
	serialno = target[0]
	for result in result_list:
		contentid = result.attrib['id']
		ok = result.attrib['state']
		if ok == '1':
			Raw.sql = "update sklcc_recheck_content set ok = 'True' where contentid = '%s'" % contentid
		else:
			Raw.sql = "update sklcc_recheck_content set ok = 'False' where contentid = '%s'" % contentid
		Raw.update( )

	Raw.sql = "select serialno from sklcc_recheck_content where contentid = '%s'" % contentid
	target = Raw.query_one( )
	serialno = target[0]

	if root.find( 'rc' ) != None:
		save_recheck_change( xml, serialno )

	Raw.sql = "update sklcc_recheck_info set state = 1 where serialno = '%s'" % serialno
	Raw.update( )
	T = Current_time( )
	Raw.sql = "update sklcc_recheck_info set leader = '%s', leader_no = '%s', assesstime = '%s'" % (
	request.session['employee'], request.session['employeeno'], T.time_str )
	Raw.update( )
	return HttpResponse( )


def pass_recheck_table( request ):
	serialno = request.GET['serialno']
	Raw = Raw_sql( )
	Raw.sql = "update sklcc_recheck_info set state = 1 where serialno = '%s'" % serialno
	Raw.update( )
	T = Current_time( )
	Raw.sql = "update sklcc_recheck_info set leader = '%s', leader_no = '%s', assesstime = '%s'" % (
	request.session['employee'], request.session['employeeno'], T.time_str )
	Raw.update( )
	return HttpResponse( )


def pass_selected_recheck_table( request ):
	serialno_list = request.GET.getlist( 'serialno' )
	Raw = Raw_sql( )
	for serialno in serialno_list:
		Raw.sql = "update sklcc_recheck_info set state = 0 where serialno = '%s'" % serialno
		Raw.update( )
	return HttpResponse( )


########################### *@*      end of recheck_choose and recheck_check     *@* ###################################
################################################*** second check ***####################################################

#############################################*** authority control ***##################################################

#authority_management Tab
def get_em_authority( ):
	em_authority_list = []
	Raw = Raw_sql( )
	Raw.sql = "select employeeno, employee, username from sklcc_employee"
	target_list = Raw.query_all( )

	if target_list != False:
		for target in target_list:
			em_authority = Em_authority( )
			em_authority.employee = target[1]
			em_authority.employeeno = target[0]
			em_authority.username = target[2]
			username = target[2]
			em_authority.button_list = []
			Raw.sql = "select distinct authorityid from sklcc_employee_authority where username = '%s'" % username
			authorityid_list = Raw.query_all( )
			if authorityid_list != False:
				for authorityid in authorityid_list:
					button = Button( )
					if ( authorityid[0] >= 6 and authorityid[0] <= 14 ) or authorityid[0] == 16 or authorityid[0] >= 18:
						button.departmentno = '201'
						button.department = '拥有'
					else:
						Raw.sql = "select departmentno from sklcc_employee_authority where username = '%s' and authorityid = %d" % (
						username, authorityid[0] )
						departmentno_list = Raw.query_all( )
						if departmentno_list != False:
							for i, departmentno in enumerate( departmentno_list ):
								temp = departmentno[0] + "&"
								button.departmentno += temp
								temp = find_department_name( departmentno[0] )
								if ( i + 1 ) % 3 == 0 or ( i + 1 ) == len( departmentno_list ):
									temp += "<br/>"
								else:
									temp += ","
								button.department += temp
					button.id = authorityid[0]
					Raw.sql = "select authorityname from sklcc_authority where authorityid = %d" % ( button.id )
					button.name = Raw.query_one( )[0]
					em_authority.button_list.append( button )
			em_authority_list.append( em_authority )

	return em_authority_list


def management( request ):
	status = request.session['status']
	if 7 in status:
		em_number = request.session['employeeno']
		username = request.session['username']
		employeename = request.session['employee']
		html = get_template( 'management.html' )
		Raw = Raw_sql( )

		Raw.sql = "select distinct employeeno, employee, username from sklcc_employee order by employeeno"
		target_list = Raw.query_all( )
		employee_list = list( )
		if target_list != False:
			for target in target_list:
				employee_info = Employee( )
				employee_info.employee = target[1]
				employee_info.employeeno = target[0]
				employee_info.username = target[2]
				employee_list.append( employee_info )

		department_list = list( )
		Raw.sql = "select departmentno, department from sklcc_department order by departmentno"
		department_list_found = Raw.query_all( )
		if department_list_found != False:
			for department in department_list_found:
				department_info = Department_info( )
				department_info.departmentname = department[1]
				department_info.departmentno = department[0]
				department_list.append( department_info )

		Raw.sql = "select * from sklcc_authority"
		target_list = Raw.query_all( )
		authority_list = []
		for target in target_list:
			temp = Authority( )
			temp.id = target[0]
			temp.name = target[1]
			temp.url = target[2]
			authority_list.append( temp )

		em_authority_list = get_em_authority( )

		Raw.sql = "select top 1  days, price_permin, bald_slowtime, EQ_return_percentage, " \
		          " form6_money_standard, form7_real_work_time, login_switch from sklcc_config"
		target = Raw.query_one( )
		days = target[0]
		price_permin = target[1]
		bald_slowtime = target[2]
		EQ_return_percentage = target[3]
		money_standard = target[4]
		real_work_time = target[5]
		login_switch = target[6]
		rule_list = []
		Raw.sql = "select employeeno, employee, typename, typeno from sklcc_employeeno_type"
		type_list = Raw.query_all( )
		if type_list != False:
			for one in type_list:
				t = Rule( )
				t.employeeno = one[0]
				t.employee = one[1]
				t.typename = one[2]
				t.typeno = one[3]
				rule_list.append( t )

		Raw.sql = "select employeeno, employee from sklcc_employee where employeeno not in ( select employeeno from sklcc_employeeno_type ) "
		target_list = Raw.query_all( )
		not_in_employee_list = []
		if target_list != False:
			for target in target_list:
				t = Employee( )
				t.employeeno = target[0]
				t.employee = target[1]
				not_in_employee_list.append( t )

		check_type_list = get_all_check_type( )
		return TemplateResponse( request, html, locals( ) )
	else:
		return HttpResponseRedirect( '/warning/' )


def add_employee( request ):
	Raw = Raw_sql( )
	employeeno = request.GET['id']
	employee = request.GET['name']
	password = request.GET['passwd']
	username = request.GET['account_name']
	authority_username = request.GET['authority']
	Raw.sql = "select * from sklcc_employee where employeeno = '%s' and username = '%s'" % ( employeeno, username )
	target = Raw.query_one( )

	if target == False:
		Raw.sql = "insert into sklcc_employee values( '%s', '%s', '%s','%s')" % (
		username, password, employee, employeeno )
		Raw.update( )
		if authority_username != "":
			Raw.sql = "select departmentno, authorityid from sklcc_employee_authority where username = '%s'" % authority_username
			authority_list = Raw.query_all( )
			if authority_list != False:
				for authority in authority_list:
					departmentno = authority[0]
					authorityid = int( authority[1] )
					Raw.sql = "insert into sklcc_employee_authority( username, departmentno, authorityid ) values( '%s', '%s', %d )" % (
					username, departmentno, int( authorityid ))
					Raw.update( )
		return HttpResponseRedirect( '/admini/?添加成功！#2' )
	else:
		return HttpResponseRedirect( '/admini/?已存在此员工！#2' )


def add_department( request ):
	departmentno = request.GET['dept_no']
	department = request.GET['dept_name']

	Raw = Raw_sql( )
	Raw.sql = "select * from sklcc_department where department = '%s' and departmentno = '%s'" % (
	department, departmentno )
	target = Raw.query_one( )
	if target == False:
		Raw.sql = "insert into sklcc_department values( '%s', '%s' )" % ( departmentno, department )
		Raw.update( )
		return HttpResponseRedirect( '/admini/?添加成功！#3' )
	else:
		return HttpResponseRedirect( '/admini/?已存在此部门！#3' )


def sync_employee_authority_change( username, username_old, control ):
	"""control = 0:delete
		control = 1, change"""
	Raw = Raw_sql( )
	if control == 0:
		Raw.sql = "delete from sklcc_employee_authority where username = '%s'" % username_old
		Raw.update( )
	else:
		Raw.sql = "update sklcc_employee_authority set username = '%s' where username = '%s'" % (username, username_old)
		Raw.update( )


def sync_employee_sklcc_record( employee, employeeno ):
	Raw = Raw_sql( )
	Raw.sql = "update sklcc_record set inspector = '%s' where inspector_no = '%s'" % ( employee, employeeno )
	Raw.update( )
	Raw.sql = "update sklcc_record set assessor = '%s' where assessor_no = '%s'" % ( employee, employeeno )
	Raw.update( )
	Raw.sql = "update sklcc_employee set employee = '%s' where employeeno = '%s'" % ( employee, employeeno )
	Raw.update( )
	Raw.sql = "update sklcc_effciency set employee = '%s' where employeeno = '%s'" % ( employee, employeeno )
	Raw.update( )
	Raw.sql = "update sklcc_employeeno_type set employee = '%s' where employeeno = '%s'" % ( employee, employeeno )
	Raw.update( )
	Raw.sql = "update sklcc_employeeno_type set recheckor = '%s' where recheckor_no = '%s'" % ( employee, employeeno )
	Raw.update( )


def sync_employee_sklcc_recheck_info( employee, employeeno ):
	Raw = Raw_sql( )
	Raw.sql = "update sklcc_recheck_info set inspector = '%s' where inspector_no = '%s'" % ( employee, employeeno )
	Raw.update( )
	Raw.sql = "update sklcc_recheck_info set recheckor = '%s' where recheckor_no = '%s'" % ( employee, employeeno )
	Raw.update( )
	Raw.sql = "update sklcc_recheck_info set leader = '%s' where leader_no = '%s'" % ( employee, employeeno )
	Raw.update( )


def add_employeeno_type( request ):
	Raw = Raw_sql( )
	rule_list = request.GET.getlist( 'item' )
	Raw.sql = 'delete from sklcc_employeeno_type'
	Raw.update( )

	for rule in rule_list:
		employee = rule.split( '>' )[1]
		employeeno = rule.split( '>' )[0]
		typeno = rule.split( '>' )[2]
		Raw.sql = "insert into sklcc_employeeno_type( employeeno, employee, typename, typeno ) values( '%s', '%s', '%s', %d )" % (
		employeeno, employee, '文胸'.decode( 'utf-8' ) if typeno == '0' else '小裤'.decode( 'utf-8' ), int( typeno ) )
		Raw.update( )

	return HttpResponseRedirect( '/admini/?修改成功！#5' )


def change_config( request ):
	days = request.GET['days']
	price_permin = float( request.GET['price'] )
	bald_slowtime = float( request.GET['bald_slowtime'] )
	EQ_return_percentage = float( request.GET['EQ_return_percentage'] )
	form6_money_standard = float( request.GET['form6_money_standard'] )
	form7_money_work_time = float( request.GET['form7_real_work_time'] )
	login_switch = 1 if 'open' in request.GET else 0
	Raw = Raw_sql( )
	Raw.sql = "update sklcc_config set days = %d, price_permin = %f, bald_slowtime = %f, EQ_return_percentage = %f," \
	          " form6_money_standard = %f, form7_real_work_time = %f, login_switch = %d" % (
	          int( days ), price_permin, bald_slowtime, EQ_return_percentage, form6_money_standard,
	          form7_money_work_time, login_switch )
	Raw.update( )

	return HttpResponseRedirect( '/admini/?修改成功！#0' )


def change_employee( request ):
	employeeno = request.GET['id']
	employee = request.GET['name']
	password = request.GET['passwd']
	username = request.GET['account_name']
	Raw = Raw_sql( )
	username_old = find_username( employeeno )

	#flag = 0:name not change
	#flag = 1:name changed
	flag = 0
	Raw.sql = "select employee from sklcc_employee where username = '%s'" % username
	target = Raw.query_one( )

	if target[0] == employee:
		flag = 0
	else:
		flag = 1

	if employee == "":
		Raw.sql = "delete from sklcc_employee where employeeno = '%s'" % employeeno
		Raw.update( )
		sync_employee_authority_change( username, username_old, 0 )
	else:
		if password == "":
			Raw.sql = "update sklcc_employee set employee = '%s', username = '%s' where employeeno = '%s'" % (
			employee, username, employeeno )
		else:
			Raw.sql = "update sklcc_employee set employee = '%s', password = '%s', username = '%s' where employeeno = '%s'" % (
			employee, password, username, employeeno )
		Raw.update( )
		sync_employee_authority_change( username, username_old, 1 )

	if flag == 1:
		sync_employee_sklcc_record( employee, employeeno )
		sync_employee_sklcc_recheck_info( employee, employeeno )
	return HttpResponseRedirect( '/admini/?修改成功！#1' )


def add_authority( request ):
	reload( sys )
	sys.setdefaultencoding( 'utf-8' )
	employeeno = request.GET['employee_no']
	authorityid = request.GET['authority_no']
	department_list = request.GET.getlist( 'dept' )
	Raw = Raw_sql( )
	Raw.sql = "select username from sklcc_employee where employeeno = '%s'" % employeeno
	username = Raw.query_one( )[0]
	for department in department_list:
		Raw.sql = "insert into sklcc_employee_authority values( '%s', %d, '%s' )" % (
		username, int( authorityid ), department )
		Raw.update( )

	return HttpResponseRedirect( '/admini/?修改成功！#5' )


def change_authority( request ):
	Raw = Raw_sql( )
	username = request.GET['username']
	item_list = request.GET.getlist( 'item' )

	if len( item_list ) == 0:
		Raw.sql = "delete from sklcc_employee_authority where username = '%s'" % ( username )
		Raw.update( )
	else:
		Raw.sql = "delete from sklcc_employee_authority where username = '%s'" % ( username )
		Raw.update( )
		for item in item_list:
			string = item.split( '>' )
			authority_id = int( string[0] )
			departmentno = string[1]
			Raw.sql = "insert into sklcc_employee_authority values( '%s', %d, '%s' )" % (
			username, authority_id, departmentno )
			Raw.update( )

	return HttpResponseRedirect( '/admini/?修改成功！#4' )


def change_department( request ):
	Raw = Raw_sql( )
	department = request.GET['dept_name']
	if department == "":
		departmentno = request.GET['dept_no']
		Raw.sql = "delete from sklcc_department where departmentno = '%s'" % departmentno
		Raw.update( )
		Raw.sql = "delete from sklcc_employee_authority where departmentno = '%s'" % departmentno
		Raw.update( )
		return HttpResponseRedirect( '/admini/?修改成功！#3' )
	else:
		departmentno = request.GET['dept_no']
		Raw.sql = "select * from sklcc_department where department = '%s'" % department
		target = Raw.query_all( )
		if target != False:
			return HttpResponseRedirect( '/admini/?数据库中已存在该部门！#3' )
		Raw.sql = "update sklcc_department set department = '%s' where departmentno = '%s'" % (
		department, departmentno )
		Raw.update( )
		return HttpResponseRedirect( '/admini/?修改成功！#3' )


def change_check_type( request ):
	Raw = Raw_sql( )
	check_type_list = request.GET.getlist( 'type' )
	Raw.sql = "delete from sklcc_check_type"
	Raw.update( )

	for one in check_type_list:
		check_id = one.split( ',' )[1]
		check_type = one.split( ',' )[0]
		if check_id == 'null':
			check_id = str( uuid.uuid1( ) )
		Raw.sql = "insert into sklcc_check_type( check_id, check_type ) values( '%s', '%s' )" % ( check_id, check_type )
		Raw.update( )

	return HttpResponseRedirect( '/admini/?修改成功！#6' )


#############################################*** authority control ***##################################################


def change_recheck_departmentno_sequence( request ):
	username = request.session['username']
	departmentno = request.GET['dept']
	departmentno_list = departmentno.split( '-' )
	Raw = Raw_sql( )
	Raw.sql = "delete from sklcc_employee_authority where username = '%s' and authorityid = 1" % username
	Raw.update( )
	for departmentno in departmentno_list:
		Raw.sql = "insert into sklcc_employee_authority values( '%s', 1, '%s' )" % ( username, departmentno )
		Raw.update( )

	return HttpResponseRedirect( '/myinfo/?修改成功！' )


def history_table( request ):
	form0_list = []
	html = get_template( 'table_haven_submitted.html' )
	em_number = request.session['employeeno']
	username = request.session['username']
	employeename = request.session['employee']
	if 'start' not in request.GET:
		url = '/history_table/'
		return TemplateResponse( request, html, locals( ) )

	start = request.GET['start'].replace( '/', '-' )
	end = request.GET['end'].replace( '/', '-' )
	if 2 or 4 or 3 or 5 in request.session['status']:
		if 2 in request.session['status']:
			form0_list += find_pre_table( request.session['employeeno'], 2, start, end )
		if 4 in request.session['status']:
			form0_list += find_pre_table( request.session['employeeno'], 4, start, end )
		if 3 in request.session['status']:
			form0_list += find_sec_table( request.session['employeeno'], 3, start, end )
		if 5 in request.session['status']:
			form0_list += find_sec_table( request.session['employeeno'], 5, start, end )

		return TemplateResponse( request, html, locals( ) )


def get_check_totalnumber( employeeno, date ):
	Raw = Raw_sql( )
	Raw.sql = "select totalnumber from sklcc_record where inspector_no = '%s' and left( createtime, 10 ) = '%s'" % (
	employeeno, date )

	totalnumber = 0
	target_list = Raw.query_all( )

	if target_list != False:
		for target in target_list:
			totalnumber += target[0]
	return totalnumber


def get_check_totalreturn( employeeno, date ):
	Raw = Raw_sql( )
	Raw.sql = "select totalreturn from sklcc_record where inspector_no = '%s' and left( createtime, 10 ) = '%s'" % (
	employeeno, date )
	totalreturn = 0
	target_list = Raw.query_all( )

	if target_list != False:
		for target in target_list:
			totalreturn += target[0]

	return totalreturn


def get_check_miss( employeeno, date ):
	Raw = Raw_sql( )
	Raw.sql = "select serialno from sklcc_recheck_info where inspector_no = '%s' and left( createtime, 10 ) = '%s'" % (
	employeeno, date )

	totalreturn = 0
	target_list = Raw.query_all( )

	if target_list != False:
		for target in target_list:
			serialno = target[0]
			Raw.sql = "select returnno from sklcc_recheck_content where serialno = '%s'" % serialno
			returnno_list = Raw.query_all( )
			if returnno_list != False:
				for returnno in returnno_list:
					totalreturn += returnno[0]

	return totalreturn


def get_check_miss_totalnumber( employeeno, date ):
	Raw = Raw_sql( )
	Raw.sql = "select serialno from sklcc_recheck_info where inspector_no = '%s' and left( createtime, 10 ) = '%s'" % (
	employeeno, date )

	totalnumber = 0
	target_list = Raw.query_all( )

	if target_list != False:
		for target in target_list:
			serialno = target[0]
			Raw.sql = "select distinct contentid, samplenumber from sklcc_recheck_content where serialno = '%s'" % serialno
			number_list = Raw.query_all( )

			if number_list != False:
				for number in number_list:
					totalnumber += number[1]

	return totalnumber


def get_recheck_totalnumber( employeeno, date ):
	Raw = Raw_sql( )
	Raw.sql = "select serialno from sklcc_recheck_info where recheckor_no = '%s' and left( createtime, 10 ) = '%s'" % (
	employeeno, date )

	totalnumber = 0
	target_list = Raw.query_all( )

	if target_list != False:
		for target in target_list:
			serialno = target[0]
			Raw.sql = "select distinct contentid, samplenumber from sklcc_recheck_content where serialno = '%s'" % serialno
			samplenumber_list = Raw.query_all( )
			if samplenumber_list != False:
				for samplenumber in samplenumber_list:
					totalnumber += samplenumber[1]

	return totalnumber


def get_recheck_serialno_totalnumber( serialno ):
	Raw = Raw_sql( )
	Raw.sql = "select distinct contentid, samplenumber from sklcc_recheck_content where serialno = '%s'" % serialno

	totalnumber = 0
	target_list = Raw.query_all( )
	if target_list != False:
		for target in target_list:
			totalnumber += target[1]

	return totalnumber


def get_recheck_serialno_totalreturn( serialno ):
	Raw = Raw_sql( )
	Raw.sql = "select returnno from sklcc_recheck_content where serialno = '%s'" % serialno

	totalreturn = 0
	target_list = Raw.query_all( )
	if target_list != False:
		for target in target_list:
			totalreturn += target[0]

	return totalreturn


def get_recheck_totalreturn( employeeno, date ):
	Raw = Raw_sql( )
	Raw.sql = "select serialno from sklcc_recheck_info where recheckor_no = '%s' and left( createtime, 10 ) = '%s'" % (
	employeeno, date )

	totalreturn = 0
	target_list = Raw.query_all( )

	if target_list != False:
		for target in target_list:
			serialno = target[0]
			Raw.sql = "select returnno from sklcc_recheck_content where serialno = '%s'" % serialno
			returnno_list = Raw.query_all( )
			if returnno_list != False:
				for returnno in returnno_list:
					totalreturn += returnno[0]

	return totalreturn


def get_myinfo( username ):
	Raw = Raw_sql( )
	Raw.sql = "select username, password, employee, employeeno from sklcc_employee where username = '%s'" % username
	target = Raw.query_one( )
	employee = Employee( )

	if target != False:
		employee.username = target[0]
		employee.password = target[1]
		employee.employee = target[2]
		employee.employeeno = target[3]

	return employee


def get_today_bald( employeeno, date ):
	Raw = Raw_sql( )
	Raw.sql = "select top 1 totalnumber from sklcc_recheck_bald where recheckor_no = '%s' and left( createtime, 10 ) = '%s'" % (
	employeeno, date )
	totalnumber = 0
	target = Raw.query_one( )

	if target != False:
		totalnumber = target[0]

	return totalnumber


def get_recheck_department( username ):
	Raw = Raw_sql( )
	Raw.sql = "select distinct departmentno from sklcc_employee_authority where username = '%s' and authorityid = 1" % username
	target_list = Raw.query_all( )
	department_list = []
	if target_list != False:
		for departmentno in target_list:
			department = Department_info( )
			department.departmentno = departmentno[0]
			department.departmentname = find_department_name( departmentno )
			department_list.append( department )

	return department_list


def get_worktime_by_batch( batch ):
	Raw = Raw_sql( )
	Raw.sql = "select producemasterid from ProduceMaster WITH (NOLOCK) where batch = '%s' and FormState = '审核'".decode(
		'utf-8' ) % batch
	res = 0.0
	target = Raw.query_one( 'MSZ' )
	if target != False:
		producemasterid = target[0]
		Raw.sql = "select slowtime from ProduceStyle WITH (NOLOCK) where producemasterid = '%s' and workname = " % producemasterid + "'检验'".decode(
			'utf-8' )
		temp = Raw.query_one( 'MSZ' )
		if temp != False:
			res = float( temp[0] )
	return res


def get_worktime_by_inspector_date( inspector_no, date, month_or_day ):
	'''moth_or_day = 1, date 为当日
	month_or_day = 0, date 为当月'''
	Raw = Raw_sql( )
	if month_or_day == 1:
		Raw.sql = "select sum(totalnumber), batch from sklcc_record where inspector_no = '%s' and left( createtime, 10 ) = '%s' group by batch" % (
		inspector_no, date )
	else:
		Raw.sql = "select sum(totalnumber), batch from sklcc_record where inspector_no = '%s' and left( createtime, 10 ) " \
		          ">= '%s' and left( createtime, 10 ) <= '%s' group by batch" % (
		          inspector_no, date[0:8] + '01', date[0:8] + '31' )
	target_list = Raw.query_all( )
	res_list = []
	if target_list != False:
		for target in target_list:
			batch = target[1]
			totalnumber = target[0]
			worktime = float( get_worktime_by_batch( batch ) * totalnumber )
			temp = { 'batch': batch, 'no': totalnumber, 'worktime': worktime }
			res_list.append( temp )
	return res_list


def myinfo( request ):
	username = request.session['username']
	em_number = request.session['employeeno']
	html = get_template( 'personal.html' )
	employeeno = request.session['employeeno']
	employeename = request.session['employee']
	employee = get_myinfo( username )

	T = Current_time( )
	today = T.get_date( )
	today_check_totalnumber = get_check_totalnumber( employeeno, today )
	today_check_totalreturn = get_check_totalreturn( employeeno, today )
	today_check_miss = get_check_miss( employeeno, today )
	today_check_miss_totalnumber = get_check_miss_totalnumber( employeeno, today )

	if today_check_totalnumber == 0:
		today_repair_percentage = '0%'
	else:
		today_repair_percentage = format( float( today_check_totalreturn ) / float( today_check_totalnumber ), '.2%' )

	if today_check_miss_totalnumber == 0:
		today_check_miss_percentage = '0%'
	else:
		today_check_miss_percentage = format( float( today_check_miss ) / float( today_check_miss_totalnumber ), '.2%' )

	today_recheck_totalnumber = get_recheck_totalnumber( employeeno, today )
	today_recheck_totalreturn = get_recheck_totalreturn( employeeno, today )

	department_list = get_recheck_department( request.session['username'] )

	bald_totalnumber = get_today_bald( employeeno, today )

	question_list = get_personal_miss_history( employeeno, today )

	worktime_list = get_worktime_by_inspector_date( employeeno, today, 1 )
	worktime_month_list = get_worktime_by_inspector_date( employeeno, today, 0 )
	worktime_today = 0.0
	worktime_month = 0.0
	for one in worktime_list:
		worktime_today += one['worktime']
	for one in worktime_month_list:
		worktime_month += one['worktime']

	return TemplateResponse( request, html, locals( ) )


def myinfo_history( request ):
	Raw = Raw_sql( )
	res_head = '<thead><tr>'
	res_body = ''
	username = request.session['username']
	employeeno = request.session['employeeno']

	start = request.GET['start']
	end = request.GET['end']
	distance = get_time_distance_list( start, end )
	distance_str = change_distance_date_to_str_have_year( distance )
	myinfo_history_list = []

	for i, date in enumerate( distance_str ):
		temp = Myinfo( employeeno, date )
		myinfo_history_list.append( temp )
	for t in myinfo_history_list:
		res_body += '<tr list=\"'
		for u in t.question_list:
			res_body += u + '<br/>'
		res_body += '\" >'
		res_body += '<td class="first"></td>'
		res_body += '<td>' + t.date + '</td>'
		res_body += '<td>' + str( t.check_totalnumber ) + '</td>'
		res_body += '<td>' + str( t.check_totalreturn ) + '</td>'
		res_body += '<td>' + t.check_percentage + '</td>'
		res_body += '<td>' + str( t.check_miss ) + '</td>'
		res_body += '<td>' + t.recheck_percentage + '</td>'
		res_body += '<td>' + str( t.recheck_totalnumber ) + '</td>'
		res_body += '<td>' + str( t.recheck_totalreturn ) + '</td>'
		res_body += '<td>' + str( t.bald_totalnumber ) + '</td>'
		res_body += '</tr>'
	res_body += '</tbody>'
	return HttpResponse( res_body )


def change_password( request ):
	username = request.session['username']
	old = request.GET['pre']
	new = request.GET['adv']
	new_rep = request.GET['adv_repeat']
	Raw = Raw_sql( )
	Raw.sql = "select password from sklcc_employee where username = '%s'" % username
	target = Raw.query_one( )
	if target != False:
		if old != target[0]:
			return HttpResponseRedirect( '/myinfo/?原密码错误！修改失败！#1' )
		elif len( new ) >= 20:
			return HttpResponseRedirect( '/myinfo/?密码位数过长！请输入少于20位的数字密码！#1' )
		elif new == old:
			return HttpResponseRedirect( '/myinfo/?原密码与新密码相同！修改失败！#1' )
		elif new != new_rep:
			return HttpResponseRedirect( '/myinfo/?两次输入的新密码不一致！请重新修改！#1' )
		else:
			Raw.sql = "update sklcc_employee set password = '%s' where username = '%s'" % ( new, username )
			Raw.update( )
			return HttpResponseRedirect( '/myinfo/?修改成功！#1' )
	else:
		return HttpResponseRedirect( '/myinfo/?用户信息有误！请联系管理员！#1' )


def return_check( request ):
	html = get_template( 'daily_return_check.html' )
	username = request.session['username']
	employeename = request.session['employee']
	em_number = request.session['employeeno']
	start = request.GET['start']
	end = request.GET['end']
	distance = get_time_distance_list( start, end )
	distance_have_year = change_distance_date_to_str_have_year( distance )

	return_check_list = []
	for date in distance_have_year:
		Raw = Raw_sql( )

		Raw.sql = "select distinct sklcc_record.serialno, batch, createtime, check_type, totalreturn, sklcc_record.inspector_no, sklcc_record.inspector, real_return, sklcc_return_check.assesstime, totalnumber," \
		          " ok, sklcc_return_check.state from sklcc_return_check, sklcc_record where" \
		          " sklcc_record.serialno = sklcc_return_check.serialno and left( createtime, 10 ) = '%s' and sklcc_record.inspector_no = '%s' order by sklcc_return_check.state asc" % (
		          date, em_number )
		target_list = Raw.query_all( )

		if target_list != False:
			for target in target_list:
				return_check_info = Return_check_info( )
				return_check_info.type = target[3]
				return_check_info.ok = target[10]
				return_check_info.serialno = target[0]
				return_check_info.batch = target[1]
				return_check_info.createtime = target[2].split( ' ' )[0]
				return_check_info.realreturn = target[7]
				return_check_info.totalreturn = target[4]
				return_check_info.totalnumber = target[9]
				return_check_info.state = target[11]
				return_check_info.question_list = []
				Raw.sql = "select questionname, questionno, returnno from sklcc_return_check where serialno = '%s'" % \
				          target[0]
				QC_list = Raw.query_all( )

				for QC in QC_list:
					temp = { }
					if QC[0] == None:
						pass
					else:
						temp['name'] = QC[0]
						temp['no'] = QC[1]
						temp['count'] = QC[2]
						return_check_info.question_list.append( temp )
				return_check_list.append( return_check_info )
	return_check_list.sort( lambda t1, t2: cmp( t1.state, t2.state ) )
	url = '/return_check/'
	question_list = get_all_question( )

	return TemplateResponse( request, html, locals( ) )


def pass_return_check( request ):
	try:
		Raw = Raw_sql( )
		json = request.POST['res']
		res = simplejson.loads( json )
		T = Current_time( )

		for one in res:
			serialno = one['serialno']
			Raw.sql = "select * from sklcc_return_check where serialno = '%s'" % serialno
			target_list = Raw.query_all( )
			if target_list != False:
				Raw.sql = "delete from sklcc_return_check where serialno = '%s'" % serialno
				Raw.update( )

			realreturn = int( one['count'] )
			ok = int( one['conclusion'] )
			question_list = one['mistakes']
			if len( question_list ) == 0:
				Raw.sql = "insert into sklcc_return_check( serialno, real_return, ok, state ) values( '%s',  %d, %d, %d )" % (
				serialno, realreturn, ok, 1  )
				Raw.update( )
			else:
				for question in question_list:
					questionname = question['name']
					questionno = int( question['no'] )
					returnno = int( question['count'] )
					Raw.sql = "insert into sklcc_return_check( serialno, real_return, ok, state, questionname, questionno, returnno, assesstime )" \
					          " values( '%s', %d, %d, %d, '%s', '%  s', %d, '%s' )" % (
					          serialno, realreturn, ok, 1, questionname, questionno, returnno, T.time_str )

					Raw.update( )
	except Exception, e:
		make_log( sys._getframe( ).f_code.co_name + ">>>" + str( e ) )
	return HttpResponse( )


def return_check_check( request ):
	html = get_template( 'daily_return_check.html' )
	Raw = Raw_sql( )
	username = request.session['username']
	employeename = request.session['employee']
	em_number = request.session['employeeno']
	departmentno_list = find_department_authority_user( username, 4 )
	start = request.GET['start']
	end = request.GET['end']
	distance = get_time_distance_list( start, end )
	distance_have_year = change_distance_date_to_str_have_year( distance )

	return_check_list = []
	for date in distance_have_year:
		for departmentno in departmentno_list:
			Raw.sql = "select sklcc_record.serialno, batch, createtime, totalreturn, sklcc_record.inspector_no, sklcc_record.inspector, real_return, sklcc_return_check.assesstime, totalnumber, ok, sklcc_return_check.state, " \
			          "check_type from sklcc_return_check, sklcc_record where" \
			          " sklcc_record.serialno = sklcc_return_check.serialno  and left( createtime, 10 ) = '%s' and departmentno = '%s' and sklcc_return_check.state = 1" % (
			          date, departmentno )
			target_list = Raw.query_all( )

			if target_list != False:
				for target in target_list:
					return_check_info = Return_check_info( )
					return_check_info.type = target[11]
					return_check_info.ok = target[9]
					return_check_info.serialno = target[0]
					return_check_info.batch = target[1]
					return_check_info.createtime = target[2].split( ' ' )[0]
					return_check_info.realreturn = target[6]
					return_check_info.totalreturn = target[3]
					return_check_info.totalnumber = target[8]
					return_check_info.state = target[10]
					return_check_info.question_list = []
					Raw.sql = "select questionname, questionno, returnno from sklcc_return_check where serialno = '%s'" % \
					          target[0]
					QC_list = Raw.query_all( )

					for QC in QC_list:
						temp = { }
						if QC[0] == None:
							pass
						else:
							temp['name'] = QC[0]
							temp['no'] = QC[1]
							temp['count'] = QC[2]
							return_check_info.question_list.append( temp )
					return_check_list.append( return_check_info )

	return_check_list.sort( lambda t1, t2: cmp( t1.state, t2.state ) )
	url = '/return_check_check/'
	question_list = get_all_question( )
	return TemplateResponse( request, html, locals( ) )


def recheck_return_check( request ):
	html = get_template( 'daily_return_check.html' )
	username = request.session['username']
	employeename = request.session['employee']
	em_number = request.session['employeeno']
	start = request.GET['start']
	end = request.GET['end']
	distance = get_time_distance_list( start, end )
	distance_have_year = change_distance_date_to_str_have_year( distance )

	return_check_list = []
	for date in distance_have_year:
		Raw = Raw_sql( )

		Raw.sql = "select sklcc_recheck_info.serialno, batch, createtime, sklcc_recheck_info.inspector_no," \
		          " sklcc_recheck_info.inspector, real_return, sklcc_return_check.assesstime, ok, sklcc_return_check.state " \
		          "from sklcc_return_check, sklcc_recheck_info" \
		          " where" \
		          " sklcc_recheck_info.serialno = sklcc_return_check.serialno and left( createtime, 10 ) = '%s' " \
		          "and sklcc_recheck_info.recheckor_no = '%s' order by sklcc_return_check.state asc" % (
		          date, em_number )

		target_list = Raw.query_all( )

		if target_list != False:
			for target in target_list:
				return_check_info = Return_check_info( )
				return_check_info.ok = target[7]
				return_check_info.serialno = target[0]
				return_check_info.batch = target[1]
				return_check_info.createtime = target[2].split( ' ' )[0]
				return_check_info.realreturn = target[5]
				return_check_info.state = target[8]
				return_check_info.type = "抽验"
				return_check_info.totalreturn = get_recheck_serialno_totalreturn( target[0] )
				return_check_info.totalnumber = get_recheck_serialno_totalnumber( target[0] )
				return_check_info.question_list = []
				Raw.sql = "select questionname, questionno, returnno from sklcc_return_check where serialno = '%s'" % \
				          target[0]
				QC_list = Raw.query_all( )

				for QC in QC_list:
					temp = { }
					if QC[0] == None:
						pass
					else:
						temp['name'] = QC[0]
						temp['no'] = QC[1]
						temp['count'] = QC[2]
						return_check_info.question_list.append( temp )
				return_check_list.append( return_check_info )

	return_check_list.sort( lambda t1, t2: cmp( t1.state, t2.state ) )
	url = '/recheck_return_check/'
	question_list = get_all_question( )
	return TemplateResponse( request, html, locals( ) )


def recheck_return_check_check( request ):
	html = get_template( 'daily_return_check.html' )
	username = request.session['username']
	employeename = request.session['employee']
	em_number = request.session['employeeno']
	Raw = Raw_sql( )
	departmentno_list = find_department_authority_user( username, 5 )
	start = request.GET['start']
	end = request.GET['end']
	distance = get_time_distance_list( start, end )
	distance_have_year = change_distance_date_to_str_have_year( distance )

	return_check_list = []
	for date in distance_have_year:
		for departmentno in departmentno_list:
			Raw.sql = "select sklcc_recheck_info.serialno, batch, createtime, sklcc_recheck_info.inspector_no," \
			          " sklcc_recheck_info.inspector, real_return, sklcc_return_check.assesstime, ok, sklcc_return_check.state" \
			          " from sklcc_return_check, sklcc_recheck_info where" \
			          " sklcc_recheck_info.serialno = sklcc_return_check.serialno and left( createtime, 10 ) = '%s' and departmentno = '%s' and sklcc_return_check.state = 1" % (
			          date, departmentno, )
			target_list = Raw.query_all( )

			if target_list != False:
				for target in target_list:
					return_check_info = Return_check_info( )
					return_check_info.type = "抽验"
					return_check_info.ok = target[7]
					return_check_info.serialno = target[0]
					return_check_info.batch = target[1]
					return_check_info.createtime = target[2].split( ' ' )[0]
					return_check_info.realreturn = target[5]
					return_check_info.state = target[8]
					return_check_info.totalreturn = get_recheck_serialno_totalreturn( target[0] )
					return_check_info.totalnumber = get_recheck_serialno_totalnumber( target[0] )
					return_check_info.question_list = []
					Raw.sql = "select questionname, questionno, returnno from sklcc_return_check where serialno = '%s'" % \
					          target[0]
					QC_list = Raw.query_all( )

					for QC in QC_list:
						temp = { }
						if QC[0] == None:
							pass
						else:
							temp['name'] = QC[0]
							temp['no'] = QC[1]
							temp['count'] = QC[2]
							return_check_info.question_list.append( temp )
					return_check_list.append( return_check_info )

	return_check_list.sort( lambda t1, t2: cmp( t1.state, t2.state ) )
	url = '/recheck_return_check_check/'
	question_list = get_all_question( )
	return TemplateResponse( request, html, locals( ) )
