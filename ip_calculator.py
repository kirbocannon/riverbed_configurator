from __future__ import print_function
import csv
import os
import re


# A Visio diagram is most helpful for choosing the correct networks
# Left net will be old network used for connection from WA01 to CR1-unit 1
# Right net will be old network used for connection from WA01 to CR-unit 2
# The two additional networks at the site will be unused if applicable
#left_net = '172.19.21.0/28'
#right_net = '172.19.21.16/28'

#left_net = '172.19.43.112/28'
#right_net = '172.19.43.128/28'
#cr_hostname = 'RCOG01CR11'
#cr_hostname_two = 'RCOG01CR12'

#model = '4510' # 4510, 6501 (check models), or 3850
#mode = '' # hsrp or stacked
# interfaces on WA that connect to the CR. This could be different at each site. Some interfaces
# are gi0/1, gi0/0/1, etc.
#wa02_to_gi_1_40_cr1 = 'Gi0/0/1'
#wa01_to_gi_1_46_cr1 = 'Gi0/0/2'
#wa01_to_gi_2_40_cr2 = 'Gi0/0/1'
#wa02_to_gi_2_46_cr2 = 'Gi0/0/2'


def rbed_calc_left_ips(net):

    subnet = net.split('/')[0]
    subnet_hsrp_left_cr = net.split('/')[0] # only for hsrp use
    subnet_hsrp_right_cr = net.split('/')[0] # only for hsrp use
    split_subnet = subnet.split('.')
    split_hsrp_subnet_left_cr = subnet_hsrp_left_cr.split('.') #only for hsrp use
    split_hsrp_subnet_right_cr = subnet_hsrp_right_cr.split('.') #only for hsrp use
    add_one = str(int(split_subnet[3]) + 1)
    add_five = str(int(split_subnet[3]) + 5)
    add_six = str(int(split_subnet[3]) + 6)
    add_eight = str(int(split_subnet[3]) + 8)
    split_subnet.pop(-1)
    add_one_split_ip = list(split_subnet)
    add_five_split_ip = list(split_subnet)
    add_six_split_ip = list(split_subnet)
    add_eight_split_ip = list(split_subnet)
    add_one_split_ip.append(add_one)
    add_five_split_ip.append(add_five)
    add_six_split_ip.append(add_six)
    add_eight_split_ip.append(add_eight)
    left_ip_dict = {

        'switch': 'CR-unit1-side',
        'vlan_203': '.'.join(add_one_split_ip) + ' ' +  '255.255.255.240',
        'vlan_203_sh': '.'.join(add_one_split_ip), # for sh config
        'wa02_to_cr_1': '.'.join(add_five_split_ip) + ' ' + '255.255.255.240',
        'wa01_to_cr_1': '.'.join(add_six_split_ip) + ' ' + '255.255.255.240',
        'ospf_wa02_to_cr_1': '.'.join(add_five_split_ip),
        'ospf_wa01_to_cr_1': '.'.join(add_six_split_ip),
        'wo_inpath_2_0': '.'.join(add_eight_split_ip)

    }
    # if running HSRP
    if mode == 'hsrp':
        # # add vlan 203's individual addresses to both CRs if running hsrp
        add_thirteen = str(int(split_hsrp_subnet_left_cr[3]) + 13)
        add_fourteen = str(int(split_hsrp_subnet_right_cr[3]) + 14)
        split_hsrp_subnet_left_cr.pop(-1)
        split_hsrp_subnet_right_cr.pop(-1)
        add_thirteen_split_ip = list(split_hsrp_subnet_left_cr)
        add_fourteen_split_ip = list(split_hsrp_subnet_left_cr)
        add_thirteen_split_ip.append(add_thirteen)
        add_fourteen_split_ip.append(add_fourteen)
        left_ip_dict['left_cr_svi_ip_vlan_203'] = '.'.join(add_thirteen_split_ip) + ' ' + '255.255.255.240'
        left_ip_dict['right_cr_svi_ip_vlan_203'] = '.'.join(add_fourteen_split_ip) + ' ' + '255.255.255.240'
        left_ip_dict['vlan_203_hsrp'] = '.'.join(add_one_split_ip)
    return left_ip_dict


def rbed_calc_right_ips(net):
    ''' Calculate IPs on CR based on IP standard for WAN/LAN links
        This is all right network connections '''

    subnet = net.split('/')[0]
    subnet_hsrp_left_cr = net.split('/')[0] # only for hsrp use
    subnet_hsrp_right_cr = net.split('/')[0] # only for hsrp use
    split_subnet = subnet.split('.')
    split_hsrp_subnet_left_cr = subnet_hsrp_left_cr.split('.') #only for hsrp use
    split_hsrp_subnet_right_cr = subnet_hsrp_right_cr.split('.') #only for hsrp use
    add_one = str(int(split_subnet[3]) + 1)
    add_five = str(int(split_subnet[3]) + 5)
    add_six = str(int(split_subnet[3]) + 6)
    add_eight = str(int(split_subnet[3]) + 8)
    split_subnet.pop(-1)
    add_one_split_ip = list(split_subnet)
    add_five_split_ip = list(split_subnet)
    add_six_split_ip = list(split_subnet)
    add_eight_split_ip = list(split_subnet)
    add_one_split_ip.append(add_one)
    add_five_split_ip.append(add_five)
    add_six_split_ip.append(add_six)
    add_eight_split_ip.append(add_eight)
    right_ip_dict = {

        'switch': 'CR-unit2-side',
        'vlan_213': '.'.join(add_one_split_ip) + ' ' +  '255.255.255.240',
        'vlan_213_sh': '.'.join(add_one_split_ip), # for steelhead config
        'wa02_to_cr_2': '.'.join(add_five_split_ip) + ' ' + '255.255.255.240',
        'wa01_to_cr_2': '.'.join(add_six_split_ip) + ' ' + '255.255.255.240',
        'ospf_wa02_to_cr_2': '.'.join(add_five_split_ip),
        'ospf_wa01_to_cr_2': '.'.join(add_six_split_ip),
        'wo_inpath_3_0': '.'.join(add_eight_split_ip),
        'none': 'empty'

    }
    # if running HSRP
    if mode == 'hsrp':
        # add vlan 213's individual addresses to both CRs if running hsrp
        add_thirteen = str(int(split_hsrp_subnet_left_cr[3]) + 13)
        add_fourteen = str(int(split_hsrp_subnet_right_cr[3]) + 14)
        split_hsrp_subnet_left_cr.pop(-1)
        split_hsrp_subnet_right_cr.pop(-1)
        add_thirteen_split_ip = list(split_hsrp_subnet_left_cr)
        add_fourteen_split_ip = list(split_hsrp_subnet_left_cr)
        add_thirteen_split_ip.append(add_thirteen)
        add_fourteen_split_ip.append(add_fourteen)
        right_ip_dict['left_cr_svi_ip_vlan_213'] = '.'.join(add_thirteen_split_ip) + ' ' + '255.255.255.240'
        right_ip_dict['right_cr_svi_ip_vlan_213'] = '.'.join(add_fourteen_split_ip) + ' ' + '255.255.255.240'
        right_ip_dict['vlan_213_hsrp'] = '.'.join(add_one_split_ip)
    return right_ip_dict

def analyze_hostname(hostname):
    try:
        regex_net_type = re.compile(r"^.")
        regex_site_code_split = re.split(regex_net_type, hostname)
        regex_site_code_split = regex_site_code_split[1]
        regex_site_code = re.compile(r"^...")
        regex_floor = re.compile(r"[0-9][0-9]")
        regex_function_split = re.split(regex_floor, hostname)
        regex_function_split = regex_function_split[1]
        regex_device_num = re.compile(r"[0-9][0-9]$")
        net_type = regex_net_type.match(hostname).group().upper()
        site_code = regex_site_code.match(regex_site_code_split).group().upper()
        floor = regex_floor.search(hostname).group()
        device_num = regex_device_num.search(hostname).group()
        function = regex_function_split.upper()
        analyzed_hostname = {
            'net_type': net_type,
            'site_code': site_code,
            'floor': floor,
            'device_num': device_num,
            'function': function
        }
        return analyzed_hostname
    except:
        print("Cannot analyze hostname.")


def replace_var(config_file, temp_var, var):
    ''' replace variables denoted with $ in the configuration file '''
    with open(config_file, 'r') as f:
        filedata = f.read()
    with open(config_file, 'w+') as f:
        filedata = filedata.replace(temp_var, var)
        f.writelines(filedata)

def import_csv_data():
    '''Read data in CSV'''
    with open(csv_file, 'rb') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        rb_items = list()
        for row in csv_reader:
            rb_items.append({
                'cr_1_hostname': row['cr_1_hostname'],
                'cr_2_hostname': row['cr_2_hostname'],
                'cr_model': row['cr_model'],
                'network_1_(left)': row['network_1_(left)'],
                'network_2_(right)': row['network_2_(right)'],
                'sh_primary_ip': row['sh_primary_ip'],
                'sh_pri_gateway': row['sh_pri_gateway'],
                'wa02_to_gi_1_40_cr1_interface': row['wa02_to_gi_1_40_cr1_interface'],
                'wa01_to_gi_1_46_cr1_interface': row['wa01_to_gi_1_46_cr1_interface'],
                'wa02_to_gi_2_40_cr2_interface': row['wa02_to_gi_2_40_cr2_interface'],
                'wa01_to_gi_2_46_cr2_interface': row['wa01_to_gi_2_46_cr2_interface']
            })
        return rb_items

if __name__ == '__main__':
    # get variables from CSV
    csv_file = 'riverbed_info.csv'
    rb_items = import_csv_data()
    for rb in rb_items:
        left_net = rb['network_1_(left)']
        right_net = rb['network_2_(right)']
        sh_primary_ip = rb['sh_primary_ip']
        sh_pri_gateway = rb['sh_pri_gateway']
        cr_hostname = rb['cr_1_hostname']
        cr_hostname_two = rb['cr_2_hostname']

        model = rb['cr_model']  # 4510, 6501 (check models), or 3850
        mode = ''  # hsrp or stacked
        # interfaces on WA that connect to the CR. This could be different at each site. Some interfaces
        # are gi0/1, gi0/0/1, etc.
        wa02_to_gi_1_40_cr1 = rb['wa02_to_gi_1_40_cr1_interface']
        wa01_to_gi_1_46_cr1 = rb['wa01_to_gi_1_46_cr1_interface']
        wa02_to_gi_2_40_cr2 = rb['wa02_to_gi_2_40_cr2_interface']
        wa01_to_gi_2_46_cr2 = rb['wa01_to_gi_2_46_cr2_interface']

        # create configuration file from base template. Overwrite if configuration file with same name already exists
        # Base template/config_file name and variables  will be determined by the mode the switch is running in
        # at the time of the riverbed bridge mode conversion
        if model == '4510':
            mode = 'hsrp'
            base_template_cr = '4510_hsrp_template.txt'  # for 4510 switches in stacked mode
            config_file_cr = '{}-{}.txt'.format(cr_hostname, cr_hostname_two)
        elif model == '6501':
            mode = 'hsrp'
            base_template_cr = '6501_hsrp_template.txt'  # for 4510 switches in stacked mode
            config_file_cr = '{}-{}.txt'.format(cr_hostname, cr_hostname_two)
        elif model == '3850':
            mode = 'stacked'
            base_template_cr = '3850_stacked_template.txt'  # for 3850 switches in stacked mode
            config_file_cr = '{}.txt'.format(cr_hostname)

        rbed_left_ips = rbed_calc_left_ips(left_net)
        rbed_right_ips = rbed_calc_right_ips(right_net)
        analyzed_hostname = analyze_hostname(cr_hostname)
        floor = analyzed_hostname.get('floor')
        site_code = analyzed_hostname.get('site_code')
        sh_hostname = 'O{}{}WO01'.format(site_code, floor)
        # cr configuration file generation
        try:
            with open(base_template_cr, 'r') as bt:
                lines = bt.readlines()
                with open(config_file_cr, 'w+') as f:
                    f.writelines(lines)

            # Write all variables to configuration files

            # The following is only used in hsrp configurations.
            # This will write to file the  svi ips for left CR and right CR.
            # Also generate hsrp addresses for both units.
            replace_var(config_file_cr, '$sh_hostname', sh_hostname)
            replace_var(config_file_cr, '$vlan_203_hsrp', rbed_left_ips.get('vlan_203_hsrp'))
            replace_var(config_file_cr, '$vlan_213_hsrp', rbed_right_ips.get('vlan_213_hsrp'))
            replace_var(config_file_cr, '$vlan_203', rbed_left_ips.get('vlan_203'))
            replace_var(config_file_cr, '$vlan_213', rbed_right_ips.get('vlan_213'))
            replace_var(config_file_cr, '$left_cr_svi_ip_vlan_203', rbed_left_ips.get('left_cr_svi_ip_vlan_203'))
            replace_var(config_file_cr, '$right_cr_svi_ip_vlan_203', rbed_left_ips.get('right_cr_svi_ip_vlan_203'))
            replace_var(config_file_cr, '$left_cr_svi_ip_vlan_213', rbed_right_ips.get('left_cr_svi_ip_vlan_213'))
            replace_var(config_file_cr, '$right_cr_svi_ip_vlan_213', rbed_right_ips.get('right_cr_svi_ip_vlan_213'))
            replace_var(config_file_cr, '$wa02_to_gi_1_40_cr1', wa02_to_gi_1_40_cr1)
            replace_var(config_file_cr, '$wa01_to_gi_1_46_cr1', wa01_to_gi_1_46_cr1)
            replace_var(config_file_cr, '$wa02_to_gi_2_40_cr2', wa02_to_gi_2_40_cr2)
            replace_var(config_file_cr, '$wa01_to_gi_2_46_cr2', wa01_to_gi_2_46_cr2)
            replace_var(config_file_cr, '$cr_hostname', cr_hostname)
            replace_var(config_file_cr, '$cr_hostname_two', cr_hostname_two)
            replace_var(config_file_cr, '$site_code', site_code)
            replace_var(config_file_cr, '$floor', analyzed_hostname.get('floor'))
        except:
            print("Could not generate/parse cr switch/router configuration correctly. There may be errors." )



        # WA configuration file generation
        wa1_hostname = 'R{}{}WA01'.format(site_code, floor)
        wa2_hostname = 'R{}{}WA02'.format(site_code, floor)
        config_file_wa = '{}-{}'.format(wa1_hostname, wa2_hostname)
        base_template_wa = 'generic_wa_router_template.txt'
        try:
            with open(base_template_wa, 'r') as bt:
                lines = bt.readlines()
                with open(config_file_wa, 'w+') as f:
                    f.writelines(lines)

            replace_var(config_file_wa, '$wa1_hostname', wa1_hostname)
            replace_var(config_file_wa, '$wa2_hostname', wa2_hostname)
            replace_var(config_file_wa, '$cr_hostname', cr_hostname)
            replace_var(config_file_wa, '$wa02_to_cr_1', rbed_left_ips.get('wa02_to_cr_1'))
            replace_var(config_file_wa, '$wa02_to_cr_2', rbed_right_ips.get('wa02_to_cr_2'))
            replace_var(config_file_wa, '$ospf_wa02_to_cr_1', rbed_left_ips.get('ospf_wa02_to_cr_1'))
            replace_var(config_file_wa, '$ospf_wa02_to_cr_2', rbed_right_ips.get('ospf_wa02_to_cr_2'))
            replace_var(config_file_wa, '$wa02_to_gi_1_40_cr1', wa02_to_gi_1_40_cr1)
            replace_var(config_file_wa, '$wa01_to_gi_1_46_cr1', wa01_to_gi_1_46_cr1)
            replace_var(config_file_wa, '$wa02_to_gi_2_40_cr2', wa02_to_gi_2_40_cr2)
            replace_var(config_file_wa, '$wa01_to_gi_2_46_cr2', wa01_to_gi_2_46_cr2)
        except:
            print("Could not generate/parse wa router configuration correctly. There may be errors.")

        # riverbed configuration file generation
        config_file_sh = "{}".format(sh_hostname)
        base_template_sh = 'riverbed_steelhead_template.txt'
        try:
            with open(base_template_sh, 'r') as bt:
                lines = bt.readlines()
                with open(config_file_sh, 'w+') as f:
                    f.writelines(lines)
            replace_var(config_file_sh, '$wo_inpath_2_0', rbed_left_ips.get('wo_inpath_2_0'))
            replace_var(config_file_sh, '$wo_inpath_3_0', rbed_right_ips.get('wo_inpath_3_0'))
            replace_var(config_file_sh, '$sh_hostname', sh_hostname)
            replace_var(config_file_sh, '$site_code', site_code)
            replace_var(config_file_sh, '$sh_primary_ip', sh_primary_ip)
            replace_var(config_file_sh, '$sh_pri_gateway', sh_pri_gateway)
            replace_var(config_file_sh, '$vlan_203_sh', rbed_left_ips.get('vlan_203_sh'))
            replace_var(config_file_sh, '$vlan_213_sh', rbed_right_ips.get('vlan_213_sh'))
        except:
            print("Could not generate/parse riverbed configuration correctly. There may be errors.")


# output help diagram
        print(
            '''

    CR U1--(gi1/0/46)----(vlan 211: {4:12}  --- > vlan201 )-----------( {0:12} )-----( {9} )------WA01
    CR U1--(gi1/0/40)----(vlan 211: {4:12}  --- > vlan201 )-----------( {1:12} )-----( {8} )------WA02

    CR U2--(gi1/0/46)----(vlan 213: {5:12}  --- > vlan203 )-----------( {2:12} )-----( {11}) ------WA01
    CR vU2--(gi1/0/40)----(vlan 213: {5:12} --- > vlan203 )-----------( {3:12} )-----( {10} )------WA02

    inpath2_0: {6}
    inpath3_0: {7}

            '''.format(
                    rbed_left_ips.get('wa01_to_cr_1').split(' ')[0],
                    rbed_left_ips.get('wa02_to_cr_1').split(' ')[0],
                    rbed_right_ips.get('wa01_to_cr_2').split(' ')[0],
                    rbed_right_ips.get('wa02_to_cr_2').split(' ')[0],
                    rbed_left_ips.get('vlan_203').split(' ')[0],
                    rbed_right_ips.get('vlan_213').split(' ')[0],
                    rbed_left_ips.get('wo_inpath_2_0'),
                    rbed_right_ips.get('wo_inpath_3_0'),
                    wa02_to_gi_1_40_cr1,
                    wa01_to_gi_1_46_cr1,
                    wa02_to_gi_2_40_cr2,
                    wa01_to_gi_2_46_cr2
                       )
        )






