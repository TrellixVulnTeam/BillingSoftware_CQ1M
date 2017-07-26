from django.shortcuts import render
from django.shortcuts import render_to_response
from appRegistration.forms import gymDetailsForm,memberDetailsForm,gymPlansForm,\
								memberActivatePlanForm, memberDetailsForm
from django.http import HttpResponseRedirect
import datetime
from appRegistration.models import gymDetails, memberDetails,gymPlans
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from main.views import commonDisplay
from django.db.models import Q
# Create your views here.
def dashboard(request):
	common=commonDisplay(request)
	context={}
	finalContext={**common, **context} #append the dictionaries
	return render(request,'base.html',context=finalContext)
	
@login_required
def clientRegistration(request):
	common=commonDisplay(request)
	form = gymDetailsForm(request.POST or None)
	emptyDB=True
	x=gymDetails.objects.all().values('gymNumber')
	for getLatestGymNum in x:
		emptyDB=False
		latestGymNum=getLatestGymNum

	if request.POST:
		form= gymDetailsForm(request.POST)
		if form.is_valid():
			save_it=form.save(commit = False)
			save_it.gymRegistrationDate = datetime.datetime.now()
			save_it.gymUser_id=request.user.id
			if emptyDB:
				save_it.gymNumber=1
			else:
				save_it.gymNumber= int(latestGymNum['gymNumber'])+1
			form.save()
			return HttpResponseRedirect("/client/register/")
	common=commonDisplay(request)
	context={'form':form}
	finalContext={**common, **context} #append the dictionaries
	return render(request,'registerClient.html',context=finalContext)	

@login_required
def memberRegistration(request):
	# Start: Ensure Gym is registered first
	User = get_user_model()
	userId=User.id
	gymRegistered= False
	allGymNumbers=gymDetails.objects.all().values('gymUser_id')
	for i in allGymNumbers:
		print ('---------')
		print (i['gymUser_id'])
		print (request.user.id)
		if i['gymUser_id']==request.user.id:
			gymRegistered=True
	if not gymRegistered:
		return HttpResponseRedirect("/client/register/")
	# End
	form = memberDetailsForm(request.POST or None)
	emptyDB=True
	x=memberDetails.objects.all().values('memberNumber')
	gymObj=gymDetails.objects.filter(gymUser_id=request.user.id).values()
	for elements in gymObj:
		gymNumber=elements['gymNumber']
	
	for getMemberGymNum in x:
		emptyDB=False
		latestMemberNum=getMemberGymNum

	if request.POST:
		form= memberDetailsForm(request.POST)
		print ('inside post')
		if form.is_valid():
			print ('inside form')
			save_it=form.save(commit = False)
			save_it.memberRegistrationDate = datetime.datetime.now()
			save_it.memberGymNumber_id=gymNumber
			if emptyDB:
				save_it.memberNumber=1
			else:
				save_it.memberNumber= int(latestMemberNum['memberNumber'])+1
			form.save()
			return HttpResponseRedirect("/hello/")
	common=commonDisplay(request)
	context={'form':form}
	finalContext={**common, **context} #append the dictionaries
	return render(request,'registerMembers.html',context=finalContext)

def clientPlans(request):
	# Start: Ensure Gym is registered first
	User = get_user_model()
	userId=User.id
	gymRegistered= False
	allGymNumbers=gymDetails.objects.all().values('gymUser_id')
	for i in allGymNumbers:
		print ('---------')
		print (i['gymUser_id'])
		print (request.user.id)
		if i['gymUser_id']==request.user.id:
			gymRegistered=True
	if not gymRegistered:
		return HttpResponseRedirect("/client/register/")
	# End
	common=commonDisplay(request)
	form = gymPlansForm(request.POST or None)
	if request.POST:
		if form.is_valid():
			save_it=form.save(commit = False)
			gymObj=memberDetails.objects.filter(gymUser_id=request.user.id).values()
			for elements in gymObj:
				gymNumber=elements['gymNumber']
				save_it.planGymNumber_id= gymNumber
			form.save()
			return HttpResponseRedirect("/client/plans/")
	common=commonDisplay(request)
	context={'form':form}
	finalContext={**common, **context} #append the dictionaries
	return render(request,'gymPlans.html',context=finalContext)

def clientActivatePlan(request):
	form = memberActivatePlanForm(request.POST or None)
	context={'form':form}

	if form.is_valid():
		print ('******')
		input=form.cleaned_data['searchUser']
		print (input)
		member=memberDetails.objects.filter(memberContactNumber=input).values()
		for i in member:
			name=i['memberName']
			memberEmail=i['memberEmail']
			registrationDate=i['memberRegistrationDate']
			status=i['memberStatus']
			memberId=i['memberGymNumber_id']
			
			gymObj=gymDetails.objects.filter(gymUser_id=request.user.id).values()
			for i in gymObj:
				gymNumber= i['gymNumber']
		
			Plans=gymPlans.objects.filter(planGymNumber_id=gymNumber).values()
			planNames=[]
			for names in Plans:
				planNames.append(names['planName'])
			print ('gymplans:', planNames)

			context={'form':form,'name':name,'memberEmail':memberEmail,'registrationDate':registrationDate,
					'status':status,'memberId':memberId,'plans':planNames}
		# save_it=form.save(commit = False)
		# gymObj=gymDetails.objects.filter(Q(memberContactNumber=owner) | Q(moderated=False)).values()
		# for elements in gymObj:
		# 	gymNumber=elements['gymNumber']
		# 	save_it.planGymNumber_id= gymNumber
		# form.save()
		#return HttpResponseRedirect("/client/activateplan/")
	common=commonDisplay(request)
	
	finalContext={**common, **context} #append the dictionaries
	return render(request,'gymPlans.html',context=finalContext)