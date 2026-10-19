from datetime import datetime

from sqlmodel import SQLModel, Session
from pydantic import ValidationError

from carsipdb.sqlmodels import (
    Device,
    Computer,
    DHCP,
    DNS,
    Tag,
    Location,
    Sector,
    Interface,
    CPU,
    Memory,
    MemorySlot,
    OS,
    PhysicalDisk,
    PhysicalDiskType,
    Volume,
    Firmware,
    PortType,
    VLAN,
    MAC,
    IP,
    Neighbor,
    Switch,
    Port,
    PortFDB,
)


# Creates test data in JSON form and validates using Pydantic before adding to the DB
def sqlmodel_validate_data(reset, engine) -> None:
    if reset:
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)

    timestamp = datetime.now()

    with Session(engine) as session, session.begin():
        # Sector
        s13 = {"name": "13", "modify_time": timestamp, "create_time": timestamp}
        s14 = {"name": "14", "modify_time": timestamp, "create_time": timestamp}
        s15 = {"name": "15", "modify_time": timestamp, "create_time": timestamp}
        # Location
        l13 = {"name": "13 LOM", "modify_time": timestamp, "create_time": timestamp}
        l14 = {"name": "14 LOM", "modify_time": timestamp, "create_time": timestamp}
        l15 = {"name": "15 LOM", "modify_time": timestamp, "create_time": timestamp}
        testtag = {"name": "Test Device", "modify_time": timestamp, "create_time": timestamp}
        testmem = {"capacity": 32, "speed": 5600, "modify_time": timestamp, "create_time": timestamp}
        testcpu = {
            "model": "Intel Xeon Gold 5415+",
            "clock_speed": 2900,
            "physical_cores": 8,
            "logical_cores": 16,
            "modify_time": timestamp,
            "create_time": timestamp,
        }
        testos = {"name": "Microsoft Windows 11 Enterprise", "version": "10.0.26200.8457", "build": "25H2", "modify_time": timestamp, "create_time": timestamp}
        testdisktype = {"model": "Intel Raid 1 Volume", "capacity": 954, "type": "SSD", "modify_time": timestamp, "create_time": timestamp}
        testfirmware = {"name": "Example Firmware", "modify_time": timestamp, "create_time": timestamp}
        testporttype = {"name": "Example port type", "modify_time": timestamp, "create_time": timestamp}
        testvlan = {"name": "Example VLAN", "modify_time": timestamp, "create_time": timestamp}
        try:
            sector_13 = Sector.model_validate(s13)
            sector_14 = Sector.model_validate(s14)
            sector_15 = Sector.model_validate(s15)
            lom_13 = Location.model_validate(l13)
            lom_14 = Location.model_validate(l14)
            lom_15 = Location.model_validate(l15)
            test_tag = Tag.model_validate(testtag)
            test_mem = Memory.model_validate(testmem)
            test_cpu = CPU.model_validate(testcpu)
            win11 = OS.model_validate(testos)
            test_disktype = PhysicalDiskType.model_validate(testdisktype)
            test_firmware = Firmware.model_validate(testfirmware)
            test_porttype = PortType.model_validate(testporttype)
            test_vlan = VLAN.model_validate(testvlan)
        except ValidationError as e:
            print("The following data failed to validate: ")
            print(e.json())

        session.add_all([sector_13, sector_14, sector_15, lom_13, lom_14, lom_15, test_tag, test_mem, test_cpu, win11, test_disktype, test_firmware, test_porttype, test_vlan])
        # Examples used: CARS5 and CHEMMAT-F126
        device = {
            "location_id": 1,
            "sector_id": 1,
            "description": "Test",
            "name": "Test",
            "make": "Test",
            "model": "Test",
            "serial_number": "Test",
            "uptime": 3,
            "last_online": timestamp,
            "status": "Test",
            "owners": "Alex",
            "modify_time": timestamp,
            "create_time": timestamp,
        }
        comp = {
            "device_id": 1,
            "bios_version": "2.48.0",
            "timezone": "(UTC-06:00) Central Time (US & Canada)",
            "reboot_pending": True,
            "cpu_count": 1,
            "memory_total": 64,
            "modify_time": timestamp,
            "create_time": timestamp,
        }
        dns = {"name": "Test", "modify_time": timestamp, "create_time": timestamp}
        dhcp = {
            "device_id": 1,
            "dns_id": 1,
            "name": "Test",
            "modify_time": timestamp,
            "create_time": timestamp,
        }
        interf = {
            "device_id": 1,
            "name": "intel Ethernet Connection (5) I219-LM",
            "manufacturer": "Intel",
            "speed": 1000,
            "status": "Connected",
            "modify_time": timestamp,
            "create_time": timestamp,
        }
        memslot = {"computer_id": 1, "memory_id": 1, "slot_number": 0, "modify_time": timestamp, "create_time": timestamp}
        disk = {"computer_id": 1, "physicaldisktype_id": 1, "smart_status": "OK", "firmware": "1.0.", "modify_time": timestamp, "create_time": timestamp}
        volume = {"physicaldisk_id": 1, "capacity": 952.6, "file_system": "NTFS", "usage": "17%", "modify_time": timestamp, "create_time": timestamp}
        mac1 = {"name": "00:11:22:33:44:55", "modify_time": timestamp, "create_time": timestamp}
        mac2 = {"name": "66:77:88:99:AA:BB", "modify_time": timestamp, "create_time": timestamp}
        ip1 = {"name": "1.2.3.4", "modify_time": timestamp, "create_time": timestamp}
        ip2 = {"name": "5.6.7.8", "modify_time": timestamp, "create_time": timestamp}
        switch = {"device_id": 1, "firmware_id": 1, "cpu_id": 1, "modify_time": timestamp, "create_time": timestamp}
        port = {
            "port_type_id": 1,
            "switch_id": 1,
            "vlan_id": 1,
            "name": "Test Port",
            "speed": 10,
            "is_online": True,
            "error_count": 0,
            "description": "Example",
            "admin_status": True,
            "is_uplink": False,
            "modify_time": timestamp, 
            "create_time": timestamp,
        }
        port2 = {
            "port_type_id": 1,
            "switch_id": 1,
            "vlan_id": 1,
            "name": "Second Port",
            "speed": 25,
            "is_online": True,
            "error_count": 0,
            "description": "Remote",
            "admin_status": False,
            "is_uplink": False,
            "modify_time": timestamp, 
            "create_time": timestamp,
        }
        fdb = {
            "vendor": "Intel",
            "port_id": 1,
            "mac_id": 1,
            "ip_id": 1,
            "modify_time": timestamp, 
            "create_time": timestamp,
        }
        neighbor = {
            "local_port_id": 1,
            "remote_port_id": 2,
            "modify_time": timestamp, 
            "create_time": timestamp,
        }
        try:
            test_device = Device.model_validate(device)
            test_computer = Computer.model_validate(comp)
            test_dns = DNS.model_validate(dns)
            test_dhcp = DHCP.model_validate(dhcp)
            test_interface = Interface.model_validate(interf)
            test_mem_slot = MemorySlot.model_validate(memslot)
            test_disk = PhysicalDisk.model_validate(disk)
            test_volume = Volume.model_validate(volume)
            test_mac1 = MAC.model_validate(mac1)
            test_mac2 = MAC.model_validate(mac2)
            test_ip1 = IP.model_validate(ip1)
            test_ip2 = IP.model_validate(ip2)
            test_switch = Switch.model_validate(switch)
            test_port1 = Port.model_validate(port)
            test_port2 = Port.model_validate(port2)
            test_fdb = PortFDB.model_validate(fdb)
            test_neighbor = Neighbor.model_validate(neighbor)
        except ValidationError as e:
            print("The following data failed to validate: ")
            print(e.json())
        """Relationships:
        One to one: Computer, Device
                    Device, DHCP
                    DHCP, DNS
                    Switch, Device
                    PortFDB, Port
                    PortFDB, MAC
                    PortFDB, IP
                    Interface, MAC
                    DNS, IP
                    DHCP, IP
                    DHCP, MAC
        Many to one: Device, Location
                     Device, Sector
                     Interface, Device
                     MemorySlot, Computer
                     MemorySlot, Memory
                     PhysicalDisk, Computer
                     PhysicalDisk, PhysicalDiskType
                     Volume, PhysicalDisk
                     Switch, Firmware
                     Port, Switch
                     Port, PortType
                     Port, VLAN
                     Switch, CPU
                     MemorySlot, Switch
        Many to many: Computer, CPU
                      Computer, OS
                      Port, Port (via Neighbors)
                      Device, Tag
        """
        test_computer.device = test_device
        test_device.dhcp = test_dhcp
        test_dhcp.dns = test_dns
        loc = session.get(Location, 1)
        if loc is None:
            print("Error: Test Location not found")
        else:
            test_device.location = loc
        sect = session.get(Sector, 1)
        if sect is None:
            print("Error: Test Sector not found")
        else:
            test_device.sector = sect
        test_interface.device = test_device
        test_mem_slot.computer = test_computer
        test_mem_slot.memory = test_mem
        test_disk.computer = test_computer
        test_disk.physical_disk_type = test_disktype
        test_volume.physical_disk = test_disk
        test_computer.cpus = [test_cpu]
        ose = session.get(OS, 1)
        if ose is None:
            print("Error: Test OS not found")
        else:
            test_computer.oses = [ose]
        test_switch.device = test_device
        test_switch.firmware = test_firmware
        test_switch.cpu = test_cpu
        test_port1.switch = test_switch
        test_port2.switch = test_switch
        test_port1.port_type = test_porttype
        test_port2.port_type = test_porttype
        test_port1.vlan = test_vlan
        test_port2.vlan = test_vlan
        test_fdb.port = test_port1
        test_fdb.mac = test_mac2
        test_fdb.ip = test_ip2

        test_interface.mac = test_mac1
        test_dns.ip = test_ip1
        test_dhcp.ip = test_ip1
        test_dhcp.mac = test_mac1

        test_device.tags = [test_tag]

        session.add_all([test_device, test_computer, test_dns, test_dhcp, test_interface, test_mem_slot, test_disk, test_volume, test_port1, test_port2, test_mac1, test_mac2, test_ip1, test_ip2, test_switch, test_fdb, test_neighbor])