#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file NaoSimpleManipulator.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

import naoqi

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
naosimplemanipulator_spec = ["implementation_id", "NaoSimpleManipulator", 
		 "type_name",         "NaoSimpleManipulator", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "pretty", 
		 "category",          "Motio", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.IPAdress", "192.168.120.23 ",
		 "conf.__widget__.IPAdress", "text",
		 ""]
# </rtc-template>

##
# @class NaoSimpleManipulator
# @brief ModuleDescription
# 
# 
class NaoSimpleManipulator(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_targetPose_LArm = RTC.TimedPose3D(RTC.Time(0,0),0)
		"""
		"""
		self._targetPose_LArmIn = OpenRTM_aist.InPort("targetPose_LArm", self._d_targetPose_LArm)
		self._d_targetPose_RArm = RTC.TimedPose3D(RTC.Time(0,0),0)
		"""
		"""
		self._targetPose_RArmIn = OpenRTM_aist.InPort("targetPose_RArm", self._d_targetPose_RArm)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  IPAdress
		 - DefaultValue: 192.168.120.23 
		"""
		self._IPAdress = ['192.168.120.23 ']
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("IPAdress", self._IPAdress, "192.168.120.23")
		
		# Set InPort buffers
		self.addInPort("targetPose_LArm",self._targetPose_LArmIn)
		self.addInPort("targetPose_RArm",self._targetPose_RArmIn)
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
                self._proxy = naoqi.ALProxy("ALMotion", self._IPAdress[0], 9559)
                self._proxy.setStiffnesses(["LArm"], 1.0)
                self._proxy.setStiffnesses(["RArm"], 1.0)


		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):

                if self._targetPose_LArmIn.isNew():
                        v = self._targetPose_LArmIn.read()
                        pose = [0.0] * 6
                        pose[0] = v.data.position.x 
                        pose[1] = v.data.position.y 
                        pose[2] = v.data.position.z 
                        self._proxy.setPositions("LArm", 0, pose, 0.3, 7)

                        currentPosition_LArm = self._proxy.getPosition("LArm", 0, True)
                        print ("LArm = " ,currentPosition_LArm)
                        time.sleep(1)


                if self._targetPose_RArmIn.isNew():
                        v = self._targetPose_RArmIn.read()
                        pose = [0.0] * 6
                        pose[0] = v.data.position.x 
                        pose[1] = v.data.position.y 
                        pose[2] = v.data.position.z 
                        self._proxy.setPositions("RArm", 0, pose, 0.3, 7)

                        currentPosition_RArm = self._proxy.getPosition("RArm", 0, True)
                        print ("RArm = " ,currentPosition_RArm)
                        time.sleep(1)
	
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def NaoSimpleManipulatorInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=naosimplemanipulator_spec)
    manager.registerFactory(profile,
                            NaoSimpleManipulator,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    NaoSimpleManipulatorInit(manager)

    # Create a component
    comp = manager.createComponent("NaoSimpleManipulator")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

