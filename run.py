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

import apicController
import os

import urllib3

if __name__ == "__main__":
    #Suppress Warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # API Setup, leave this lines here
    apicController.url = os.getenv("APIC_URL")
    apicController.token = apicController.get_token(os.getenv("APIC_USERNAME"), os.getenv("APIC_PASSWORD"))

    print("Press \n1 to create all apic objects\n 2 to delete all apic objects\n 3 to exit")
    menu_option = input(" ")
    if menu_option == "1":
        """******* APIC Objects creations *******"""

        name = "PROD_TN"
        apicController.createTenant(name)

        print("Creating CDP Policies")
        name = 'CDP_ENABLE_INTPL'
        description = 'CDP Enabled'
        adminSt = 'enabled'
        apicController.createCDPPolicies(name, description, adminSt)
        name = 'CDP_DISABLE_INTPL'
        description = 'CDP Disabled'
        adminSt = 'disabled'
        apicController.createCDPPolicies(name, description, adminSt)

        print("Creating LLDP Policies")
        name = 'LLDP_ENABLE_INTPL'
        description = 'LLDP Enabled'
        receive_state = 'enabled'
        transmit_state = 'enabled'
        apicController.createLLDPPolicies(name, description, receive_state, transmit_state)
        name = 'LLDP_DISABLE_INTPL'
        description = 'LLDP Disabled'
        receive_state = 'disabled'
        transmit_state = 'disabled'
        apicController.createLLDPPolicies(name, description, receive_state, transmit_state)

        print("Creating Interface Policies")
        name = 'L2_GLOBAL_VLAN_INTPL'
        VLAN_Scope = 'global'
        apicController.createInterfacePolicies(name, VLAN_Scope)
        name = 'L2_LOCAL_VLAN_INTPL'
        VLAN_Scope = 'portlocal'
        apicController.createInterfacePolicies(name, VLAN_Scope)

        # portchannelmember policy
        apicController.createPortChannelMemberPolicy("Default_test", '')

        print("Creating PROD_TN_GW bridge domain")
        name = 'PROD_BD_GW'
        apicController.create_PROD_TN_DefaultBridgeDomain(name)

        print("Creating Physical Domain")
        name = 'EMEA_UK_PHY_DOM'
        vlan = 'EMEA_UK_PHY_VLPL'
        apicController.create_physical_domain(name,vlan)

        print("Creating ER Domains")
        name = "EMEA_UK_L3OUT_DOM"
        vlan = "EMEA_UK_L3EXT_VLPL"
        apicController.create_ER_domain(name, vlan)
        name = "EMEA_UK_L3UD_DOM"
        vlan = "EMEA_UK_L3UD_VLPL"
        apicController.create_ER_domain(name, vlan)
        name = "EMEA_UK_L3VD_DOM"
        vlan = "EMEA_UK_L3VD_VLPL"
        apicController.create_ER_domain(name, vlan)


        print("Creating VLAN Pools")
        # Creating VLAN example
        apicController.createVlanPool("EMEA_UK_PHY_VLPL","static","Physical Interface","90","239")
        # Adding VLANs to existing pool example
        apicController.addVlantoPool("EMEA_UK_PHY_VLPL","810","820")


        print("Creating STP Policies")
        # Creating STP Policies example
        apicController.createSTPpolicy("STP_BPDU_GUARD_INTPL","BPDU Guard enabled","bpdu-guard")
        apicController.createSTPpolicy("STP_BPDU_PASS_INTPL","BPDU Guard and Filter disabled")
        apicController.createSTPpolicy("STP_BPDU_FILTER_INTPL","BPDU Filter enabled","bpdu-filter")
        apicController.createSTPpolicy("STP_BPDU_FILTER_GUARD_INTPL","BPDU Guard and Filter enabled","bpdu-guard,bpdu-filter")

        print("Creating Interface Policies")
        apicController.createInterfacePolicy("LK_40G_AUTO_INTPL","40","40 Gigabit Auto Negotiate","on")
        apicController.createInterfacePolicy("LK_10G_AUTO_INTPL", "10", "10 Gigabit Auto Negotiate","on")
        apicController.createInterfacePolicy("LK_1G_AUTO_INTPL", "1", "1 Gigabit Auto Negotiate","on")
        apicController.createInterfacePolicy("LK_10G_STATIC_INTPL", "10", "10 Gigabit Non Negotiate","off")
        apicController.createInterfacePolicy("LK_1G_STATIC_INTPL", "1", "1 Gigabit Non Negotiate","off")


        apicController.createStormPolicy("Storm_100_Pol","100","100")
        apicController.createInterfacePolicyGroupPortChannel("PC_EMEA_TEST", "LK_10G_STATIC_INTPL", "EMEA_UK_L3OUT_AEP", "LACP_ACTIVE_INTPL")
        apicController.createApplicationProfile("PROD_AP","PROD_TN")
        apicController.createVRF("PROD_VRF","PROD_TN")

        print("Creating Port Channel Policies")
        # portchannel policies
        apicController.createPortChannelPolicy("LACP_ACTIVE_INTPL","LACP Active policy","active")

        apicController.createPortChannelPolicy("LACP_PASSIVE_INTPL", "LACP Passive policy", "passive")

        apicController.createPortChannelPolicy("LACP_OFF_INTPL", "LACP Static Mode On policy", "off")

        apicController.createPortChannelPolicy("LACP_MACPIN_INTPL", "MAC Pinning Policy", "mac-pin")

        apicController.createInterfacePolicyGroup("ACCESS_EMEA_TEST")

        # VPC Interface Policy Group
        apicController.createVPCPolicyGroup("VPC_EMEA_TEST","LK_40G_AUTO_INTPL","EMEA_UK_L3OUT_AEP","LACP_PASSIVE_INTPL")

        #creating l2 transport bridge domain
        apicController.createtransportbridge("PROD_BD_L2")
        """******* END APIC Objects creations *******"""

        # Leave this line at the end

    elif menu_option == "2":
        """******* START APIC Objects deletions *******"""
        print("Deleting LLDP Policies")
        apicController.delete_lldp_policies('LLDP_ENABLE_INTPL')
        apicController.delete_lldp_policies('LLDP_DISABLE_INTPL')
        print("Deleting VLAN Pools")

        apicController.delete_vlan_pools('EMEA_UK_L3EXT_VLPL')
        apicController.delete_vlan_pools('EMEA_UK_L3UD_VLPL')
        apicController.delete_vlan_pools('EMEA_UK_L3VD_VLPL')
        apicController.delete_vlan_pools('EMEA_UK_PHY_VLPL')
        apicController.delete_vlan_pools('EMEA_UK_PRIV_VLPL')

        print("Deleting Policy Groups")

        name = 'ACCESS_EMEA_TEST'
        apicController.delete_policy_groups(name)
        name = 'PC_EMEA_TEST'
        apicController.delete_policy_groups(name)
        name = 'VPC_EMEA_TEST'
        apicController.delete_policy_groups(name)

        print("Deleting Attachable Entities")

        name = 'EMEA_UK_PHY_AEP'
        apicController.delete_attachable_entity(name)
        name = 'EMEA_UK_L3OUT_AEP'
        apicController.delete_attachable_entity(name)
        name = 'EMEA_UK_L3UD_AEP'
        apicController.delete_attachable_entity(name)
        name = 'EMEA_UK_L3VD_AEP'
        apicController.delete_attachable_entity(name)

        print("Deleting Spanning Tree Policies")

        name = 'STP_BPDU_GUARD_INTPL'
        apicController.delete_spanning_tree_policies(name)
        name = 'STP_BPDU_PASS_INTPL'
        apicController.delete_spanning_tree_policies(name)
        name = 'STP_BPDU_FILTER_INTPL'
        apicController.delete_spanning_tree_policies(name)
        name = 'STP_BPDU_FILTER_GUARD_INTPL'
        apicController.delete_spanning_tree_policies(name)

        # Delete Physical Domain
        '''apicController.delete_physical_domain('EMEA_UK_PHY_DOM')
        apicController.delete_physical_domain('EMEA_UK_L3OUT_DOM')
        apicController.delete_physical_domain('EMEA_UK_L3UD_DOM')
        apicController.delete_physical_domain('EMEA_UK_L3VD_DOM')'''

        print("Deleting Interface Policies")

        # Delete Interface Policies
        apicController.delete_interface_policies("L2_GLOBAL_VLAN_INTPL")
        apicController.delete_interface_policies("L2_LOCAL_VLAN_INTPL")

        print("Deleting Link Level Policies")

        # Delete Link Level Interface Policies
        apicController.delete_linklevel_policies("LK_40G_AUTO_INTPL")
        apicController.delete_linklevel_policies("LK_10G_AUTO_INTPL")
        apicController.delete_linklevel_policies("LK_1G_AUTO_INTPL")
        apicController.delete_linklevel_policies("LK_10G_STATIC_INTPL")
        apicController.delete_linklevel_policies("LK_1G_STATIC_INTPL")

        print("Deleting CDP Policies")

        apicController.delete_CDP_Policies("CDP_ENABLE_INTPL")
        apicController.delete_CDP_Policies("CDP_DISABLE_INTPL")

        # deleting storm policies
        apicController.delete_Storm_Policies("Storm_100_Pol")

        # deleting Prod Tenant
        apicController.delete_Prod_TN("PROD_TN")


        """******* END APIC Objects deletions *******"""
    elif menu_option == "3":
        """exit"""
    else:
        print("Invalid Input\nPress 1 to create all apic objects\n 2 to delete all apic objects\n 3 to exit ")



    # Leave this line at the end

    print("Done!")
