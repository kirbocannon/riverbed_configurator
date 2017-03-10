from __future__ import print_function


left_net = '172.19.21.0/28'
right_net = '172.19.21.16/28'


def rbed_calc_left_ips(net):

    subnet = net.split('/')[0]
    split_subnet = subnet.split('.')
    add_one = str(int(split_subnet[3]) + 1)
    add_five = str(int(split_subnet[3]) + 5)
    add_six = str(int(split_subnet[3]) + 6)
    add_eight = str(int(split_subnet[3]) + 8)
    split_subnet.pop(-1)
    add_one_lst = list(split_subnet)
    add_five_lst = list(split_subnet)
    add_six_lst = list(split_subnet)
    add_eight_lst = list(split_subnet)
    add_one_lst.append(add_one)
    add_five_lst.append(add_five)
    add_six_lst.append(add_six)
    add_eight_lst.append(add_eight)
    left_ip_dict = {

        'vlan_203': '.'.join(add_one_lst) + ' ' +  '255.255.255.240',
        'wa02_0_0_1': '.'.join(add_five_lst) + ' ' + '255.255.255.240',
        'wa01_0_0_0': '.'.join(add_six_lst) + ' ' + '255.255.255.240',
        'wo_inpath_2_0': '.'.join(add_eight_lst) + ' ' + '255.255.255.240'

    }
    return left_ip_dict


def rbed_calc_right_ips(net):

    subnet = net.split('/')[0]
    split_subnet = subnet.split('.')
    add_one = str(int(split_subnet[3]) + 1)
    add_five = str(int(split_subnet[3]) + 5)
    add_six = str(int(split_subnet[3]) + 6)
    add_eight = str(int(split_subnet[3]) + 8)
    split_subnet.pop(-1)
    add_one_lst = list(split_subnet)
    add_five_lst = list(split_subnet)
    add_six_lst = list(split_subnet)
    add_eight_lst = list(split_subnet)
    add_one_lst.append(add_one)
    add_five_lst.append(add_five)
    add_six_lst.append(add_six)
    add_eight_lst.append(add_eight)
    right_ip_dict = {

        'vlan_213': '.'.join(add_one_lst) + ' ' +  '255.255.255.240',
        'wa02_0_0_2': '.'.join(add_five_lst) + ' ' + '255.255.255.240',
        'wa01_0_0_2': '.'.join(add_six_lst) + ' ' + '255.255.255.240',
        'wo_inpath_3_0': '.'.join(add_eight_lst) + ' ' + '255.255.255.240'

    }
    return right_ip_dict


if __name__ == '__main__':
    rbed_left_ips = rbed_calc_left_ips(left_net)
    rbed_right_ips = rbed_calc_right_ips(right_net)
    print(rbed_left_ips)
    print(rbed_right_ips)
    print(rbed_left_ips.get('vlan_203'))
    print(rbed_right_ips.get('vlan_213'))



