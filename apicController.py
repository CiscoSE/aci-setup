"""
Copyright (c) 2018 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from dotenv import load_dotenv
from pathlib import Path  # python3 only
from jinja2 import Environment
from jinja2 import FileSystemLoader
import os
import requests
import json

env_path = Path('.') / 'envFile'
load_dotenv(dotenv_path=env_path)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
JSON_TEMPLATES = Environment(loader=FileSystemLoader(DIR_PATH + '/jsonTemplates'))
token = ""
url = ""


def get_token(username, password):
    """
    Returns authentication token
    :param url:
    :param username:
    :param password:
    :return:
    """
    template = JSON_TEMPLATES.get_template('login.j2.json')
    payload = template.render(username=username, password=password)
    auth = makeCall(p_url='/api/aaaLogin.json', data=payload, method="POST").json()
    login_attributes = auth['imdata'][0]['aaaLogin']['attributes']
    return login_attributes['token']


def makeCall(p_url, method, data=""):
    """
    Basic method to make a call. Please this one to all the calls that you want to make
    :param p_url: APIC URL
    :param method: POST/GET
    :param data: Payload that you want to send
    :return:
    """
    cookies = {'APIC-Cookie': token}
    if method == "POST":
        response = requests.post(url + p_url, data=data, cookies=cookies, verify=False)
    elif method == "GET":
        response = requests.get(url + p_url, cookies=cookies, verify=False)
    if 199 < response.status_code < 300:
        return response
    else:
        error_message = json.loads(response.text)['imdata'][0]['error']['attributes']['text']
        if error_message.endswith("already exists."):
            return None
        else:
            raise Exception(error_message)


def createTenant(tenant_name):
    """
    Creates a tenant in ACI
    :param tenant_name:
    :return:
    """
    template = JSON_TEMPLATES.get_template('add_tenant.j2.json')
    payload = template.render(name=tenant_name)
    makeCall(
        p_url='/api/node/mo/uni/tn-' + tenant_name + '.json',
        data=payload,
        method="POST")

def createtransportbridge(bridgename):
        template = JSON_TEMPLATES.get_template('create_l2_transport_bridge_domain.j2.json')
        payload = template.render(name=bridgename)
        makeCall(
            p_url='api/node/mo/uni/tn-PROD_TN/BD-' + bridgename + '.json',
            data=payload,
            method="POST")


def createPortChannelMemberPolicy(member_name, description):
    """
        Creates a port channel member in ACI
        :param name description:
        :return:
        """
    template = JSON_TEMPLATES.get_template('add_port_channel_member_policy.j2.json')
    payload = template.render(name=member_name, descr = description)
    makeCall(
        p_url='api/node/mo/uni/infra/lacpifp-' + member_name + '.json',
        data=payload,
        method="POST")


def createPortChannelPolicy(policyname, descr, mode):
    """
            Creates a port channel policy in ACI
            :param name description mode:
            :return:
            """
    template = JSON_TEMPLATES.get_template('add_port_channel_policy.j2.json')
    payload = template.render(name=policyname, description=descr, mode=mode)
    makeCall(
        p_url='api/node/mo/uni/infra/lacplagp-' + policyname + '.json',
        data=payload,
        method="POST")

def createInterfacePolicyGroup(intpolicyname):
    """
            Creates a port channel policy in ACI
            :param name description mode:
            :return:
            """
    template = JSON_TEMPLATES.get_template('create_interface_policy_group.j2.json')
    payload = template.render(name=intpolicyname)
    makeCall(
        p_url='api/node/mo/uni/infra/funcprof/accportgrp-' + intpolicyname + '.json',
        data=payload,
        method="POST")

def createVPCPolicyGroup(vpcname, linklevelpolicy, aeprofile, pcpolicy):
    """
    Creates a Virtual Port Channel interface policy
    :param name, linklevelpolicy, aeprofile, pcpolicy:
    :return:
    """
    template = JSON_TEMPLATES.get_template('create_vpc_policy_group.j2.json')
    payload = template.render(name=vpcname, linklevel=linklevelpolicy, aep=aeprofile, portchannel=pcpolicy)
    makeCall(
        p_url='api/node/mo/uni/infra/funcprof/accbundle-' + vpcname + '.json',
        data=payload,
        method="POST")


def createStormPolicy(name, rate, burstRate):
    """
    Create interface policy
    :param int_name:
    :param desc:
    :param intcontrol:
    :return:
    """
    template = JSON_TEMPLATES.get_template('add_storm_control_policy.j2.json')
    payload = template.render(name=name, rate=rate, burstRate=burstRate)
    makeCall(
        p_url='/api/node/mo/uni/infra/stormctrlifp-' + name + '.json',
        data=payload,
        method="POST")

def createInterfacePolicyGroupPortChannel(name, linkPol, attachProf, portChannelPol):
    """
    Create interface policy
    :param int_name:
    :param desc:
    :param intcontrol:
    :return:
    """
    template = JSON_TEMPLATES.get_template('add_interface_policy_group_port_channel.j2.json')
    payload = template.render(name=name, linkPol=linkPol, attachProf=attachProf, portChannelPol=portChannelPol)
    makeCall(
        p_url='/api/node/mo/uni/infra/funcprof/accbundle-' + name + '.json',
        data=payload,
        method="POST")


def createApplicationProfile(name, tenantName):
    """
    Create interface policy
    :param int_name:
    :param desc:
    :param intcontrol:
    :return:
    """
    template = JSON_TEMPLATES.get_template('add_application_profile.j2.json')
    payload = template.render(name=name, tenant_name=tenantName)
    makeCall(
        p_url='/api/node/mo/uni/tn-' + tenantName + '/ap-' + name + '.json',
        data=payload,
        method="POST")

def createVRF(name, tenantName):
    """
    Create interface policy
    :param int_name:
    :param desc:
    :param intcontrol:
    :return:
    """
    template = JSON_TEMPLATES.get_template('add_vrf.j2.json')
    payload = template.render(name=name, tenant_name=tenantName)
    makeCall(
        p_url='/api/node/mo/uni/tn-' + tenantName + '/ctx-' + name + '.json',
        data=payload,
        method="POST")

def create_PROD_TN_DefaultBridgeDomain(name):
    template = JSON_TEMPLATES.get_template('add_PROD_TN_default_bridge_domain.j2.json')
    payload = template.render(name=name)
    #print(payload)
    makeCall(
        p_url = 'api/node/mo/uni/tn-PROD_TN/BD-'+ name +'.json',
        data = payload,
        method="POST")

def create_physical_domain(name, vlan):
    template = JSON_TEMPLATES.get_template('add_physical_domain.j2.json')
    payload = template.render(name=name, vlan = vlan)
    # print(payload)
    makeCall(
        p_url='api/node/mo/uni/phys-' + name + '.json',
        data=payload,
        method="POST")

def create_ER_domain(name, vlan):
    template = JSON_TEMPLATES.get_template('add_ER_domain.j2.json')
    payload = template.render(name=name, vlan = vlan)
    # print(payload)
    makeCall(
        p_url='api/node/mo/uni/l3dom-' + name + '.json',
        data=payload,
        method="POST")

def delete_policy_groups(name):
    template = JSON_TEMPLATES.get_template('delete_policy_groups.j2.json')
    payload = template.render(name=name)
    # print(payload)
    makeCall(
        p_url='api/node/mo/uni/infra/funcprof/accportgrp-' + name + '.json',
        data=payload,
        method="POST")

def delete_attachable_entity(name):
    template = JSON_TEMPLATES.get_template('delete_AEP.j2.json')
    payload = template.render(name=name)
    # print(payload)
    makeCall(
        p_url='api/node/mo/uni/infra.json',
        data=payload,
        method="POST")

def delete_spanning_tree_policies(name):
    template = JSON_TEMPLATES.get_template('delete_STP_policy.j2.json')
    payload = template.render(name=name)
    # print(payload)
    makeCall(
        p_url='api/node/mo/uni/infra.json',
        data=payload,
        method="POST")

def createCDPPolicies(policyName, desc, adminStatus):
    # AddCDPPolicies
    template = JSON_TEMPLATES.get_template('add_cdp_policies_disabled.j2.json')
    payload = template.render(name=policyName, description=desc, adminSt=adminStatus)
    makeCall(
        p_url='api/node/mo/uni/infra/cdpIfP-' + policyName + '.json',
        data=payload,
        method="POST")

def createLLDPPolicies(policyName, desc, recieveState, transmitState):
    template = JSON_TEMPLATES.get_template('add_lldp_policies_disabled.j2.json')
    payload = template.render(name=policyName, description=desc, recieveSt=recieveState, transmitSt=transmitState)
    makeCall(
        p_url='api/node/mo/uni/infra/lldpIfP-' + policyName + '.json',
        data=payload,
        method="POST")

def createInterfacePolicies(policyName, scopeVLAN):
    template = JSON_TEMPLATES.get_template('add_interface_policies_port.j2.json')
    payload = template.render(name=policyName, vlanScope=scopeVLAN)
    makeCall(
        p_url='api/node/mo/uni/infra/l2IfP-' + policyName + '.json',
        data=payload,
        method="POST")


'''def delete_physical_domain(name):
    """template = JSON_TEMPLATES.get_template('delete_vlan_pools.j2.json')
    payload = template.render(name=name)"""
    makeCall(
        p_url='/api/node/mo/uni/phys-'+ name + '.json',
        method="DELETE")'''

def delete_interface_policies(name):
    template = JSON_TEMPLATES.get_template('delete_interface_policies.j2.json')
    payload = template.render(name=name)
    makeCall(
        p_url='/api/node/mo/uni/infra.json',
        data=payload,
        method="POST")


def delete_linklevel_policies(name):
    template = JSON_TEMPLATES.get_template('delete_linklevel_policies.j2.json')
    payload = template.render(name=name)
    makeCall(
        p_url='/api/node/mo/uni/infra.json',
        data=payload,
        method="POST")

def createVlanPool(pool_name, allocationtype, desc, lowvlan, upvlan):
    """
    Creates a VLAN pool in ACI
    :param pool_name:
    :param allocationtype:
    :param desc:
    :param lowvlan:
    :param upvlan:
    :return:
    """
    template = JSON_TEMPLATES.get_template('add_vlan_pool.j2.json')
    payload = template.render(name=pool_name, allocation=allocationtype, description=desc, lowervlan=lowvlan, uppervlan=upvlan)
    makeCall(
        p_url='/api/node/mo/uni/infra/vlanns-[' + pool_name + ']-' + allocationtype+'.json',
        data=payload,
        method="POST")

def createSTPpolicy(stp_name, desc, intcontrol=""):
    """
    Add VLAN range to existing VLAN pool in ACI
    :param pool_name:
    :param lowvlan:
    :param upvlan:
    :return:
    """
    template = JSON_TEMPLATES.get_template('add_stp_policy.j2.json')
    payload = template.render(name=stp_name, description=desc, interfacecontrol=intcontrol)
    makeCall(
        p_url='/api/node/mo/uni/infra/ifPol-' + stp_name + '.json',
        data=payload,
        method="POST")


def createInterfacePolicy(int_name, speeds, desc="",neg=""):
    """
    Create interface policy
    :param int_name:
    :param desc:
    :param intcontrol:
    :return:
    """
    template = JSON_TEMPLATES.get_template('add_interface_policies.j2.json')
    payload = template.render(name=int_name, speed=speeds, description=desc, negotiation=neg)
    makeCall(
        p_url='/api/node/mo/uni/infra/hintfpol-' + int_name + '.json',
        data=payload,
        method="POST")

def addVlantoPool(pool_name, lowvlan, upvlan):
    """
    Add VLAN range to existing VLAN pool in ACI
    :param pool_name:
    :param lowvlan:
    :param upvlan:
    :return:
    """
    template = JSON_TEMPLATES.get_template('add_vlan_to_pool.j2.json')
    payload = template.render(name=pool_name, lowervlan=lowvlan, uppervlan=upvlan)
    makeCall(
        p_url='/api/node/mo/uni/infra/vlanns-[' + pool_name + ']-static.json',
        data=payload,
        method="POST")

def delete_lldp_policies(name):

    template = JSON_TEMPLATES.get_template('delete_LLDP_policies.j2.json')
    payload = template.render(name=name)
    makeCall(
        p_url='/api/node/mo/uni/infra.json',
        data=payload,
        method="POST")

def delete_vlan_pools(name):

    template = JSON_TEMPLATES.get_template('delete_vlan_pools.j2.json')
    payload = template.render(name=name)
    makeCall(
        p_url='/api/node/mo/uni/infra.json',
        data=payload,
        method="POST")

def delete_CDP_Policies(name):
    template = JSON_TEMPLATES.get_template('delete_CDP_Policies.j2.json')
    payload = template.render(name=name)
    # print(payload)
    makeCall(
        p_url='api/node/mo/uni/infra.json',
        data=payload,
        method="POST")



def delete_Storm_Policies(name):
    template = JSON_TEMPLATES.get_template('delete_Storm_Policies.j2.json')
    payload = template.render(name=name)
    # print(payload)
    makeCall(
        p_url='api/node/mo/uni/infra.json',
        data=payload,
        method="POST")

def delete_Prod_TN(name):
    template = JSON_TEMPLATES.get_template('delete_Prod_TN.j2.json')
    payload = template.render(name=name)
    # print(payload)
    makeCall(
        p_url='api/node/mo/uni.json',
        data=payload,
        method="POST")