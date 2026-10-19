from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship


class Base(SQLModel, table=False):
    modify_time: datetime
    create_time: datetime

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} - {', '.join(f'{k}: {getattr(self, k)}' for k in self.model_fields)}>"


class ComputerCPULink(SQLModel, table=True):
    computer_id: int | None = Field(default=None, foreign_key="computer.id", primary_key=True)
    cpu_id: int | None = Field(default=None, foreign_key="cpu.id", primary_key=True)


class ComputerOSLink(SQLModel, table=True):
    computer_id: int | None = Field(default=None, foreign_key="computer.id", primary_key=True)
    os_id: int | None = Field(default=None, foreign_key="os.id", primary_key=True)

class DeviceTagLink(SQLModel, table=True):
    device_id: int | None = Field(default=None, foreign_key="device.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)

class Neighbor(Base, table=True):
    local_port_id: int | None = Field(default=None, foreign_key="port.id", primary_key=True)
    remote_port_id: int | None = Field(default=None, foreign_key="port.id", primary_key=True)

    local_port: "Port" = Relationship(
        back_populates="local_ports",
        sa_relationship_kwargs={"foreign_keys": "[Neighbor.local_port_id]"}
    )
    remote_port: "Port" = Relationship(
        back_populates="remote_ports",
        sa_relationship_kwargs={"foreign_keys": "[Neighbor.remote_port_id]"}
    )


class Device(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    description: str
    name: str
    make: str
    model: str
    serial_number: str
    uptime: int
    last_online: datetime
    status: str
    owners: str

    location_id: int | None = Field(default=None, foreign_key="location.id")
    sector_id: int | None = Field(default=None, foreign_key="sector.id")

    location: "Location" = Relationship(back_populates="devices")
    sector: "Sector" = Relationship(back_populates="devices")
    tags: list["Tag"] = Relationship(back_populates="devices", link_model=DeviceTagLink)
    computer: "Computer" = Relationship(back_populates="device")
    dhcp: "DHCP" = Relationship(back_populates="device")
    interfaces: list["Interface"] = Relationship(back_populates="device")
    switch: "Switch" = Relationship(back_populates="device")


class Computer(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    bios_version: str
    timezone: str
    reboot_pending: bool
    cpu_count: int
    memory_total: int

    device_id: int | None = Field(default=None, foreign_key="device.id")

    device: Device = Relationship(back_populates="computer")
    cpus: list["CPU"] = Relationship(back_populates="computers", link_model=ComputerCPULink)
    memory_slots: list["MemorySlot"] = Relationship(back_populates="computer", cascade_delete=True)
    oses: list["OS"] = Relationship(back_populates="computers", link_model=ComputerOSLink)
    physical_disks: list["PhysicalDisk"] = Relationship(back_populates="computer", cascade_delete=True)

class Switch(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    device_id: int | None = Field(default=None, foreign_key="device.id")
    firmware_id: int | None = Field(default=None, foreign_key="firmware.id")
    cpu_id: int | None = Field(default=None, foreign_key="cpu.id")

    memory_slots: list["MemorySlot"] = Relationship(back_populates="switch")
    device: Device = Relationship(back_populates="switch")
    firmware: "Firmware" = Relationship(back_populates="switches")
    cpu: "CPU" = Relationship(back_populates="switches")
    ports: list["Port"] = Relationship(back_populates="switch")

class MAC(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    dhcp: "DHCP" = Relationship(back_populates="mac")
    port_fdb: "PortFDB" = Relationship(back_populates="mac")
    interface: "Interface" = Relationship(back_populates="mac")

class IP(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    dhcp: "DHCP" = Relationship(back_populates="ip")
    dns: "DNS" = Relationship(back_populates="ip")
    port_fdb: "PortFDB" = Relationship(back_populates="ip")

class DHCP(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    device_id: int | None = Field(default=None, foreign_key="device.id")
    dns_id: int | None = Field(default=None, foreign_key="dns.id")
    mac_id: int | None = Field(default=None, foreign_key="mac.id")
    ip_id: int | None = Field(default=None, foreign_key="ip.id")

    device: Device = Relationship(back_populates="dhcp")
    dns: "DNS" = Relationship(back_populates="dhcp")
    mac: MAC = Relationship(back_populates="dhcp")
    ip: IP = Relationship(back_populates="dhcp")


class DNS(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    ip_id: int | None = Field(default=None, foreign_key="ip.id")

    dhcp: DHCP = Relationship(back_populates="dns")
    ip: IP = Relationship(back_populates="dns")

class Tag(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    devices: list[Device] = Relationship(back_populates="tags", link_model=DeviceTagLink)


class Location(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    devices: list[Device] = Relationship(back_populates="location")


class Sector(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    devices: list[Device] = Relationship(back_populates="sector")


class Interface(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    manufacturer: str
    speed: int
    status: str

    device_id: int | None = Field(default=None, foreign_key="device.id")
    mac_id: int | None = Field(default=None, foreign_key="mac.id")

    device: Device = Relationship(back_populates="interfaces")
    mac: MAC = Relationship(back_populates="interface")


class CPU(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    model: str
    clock_speed: int
    physical_cores: int
    logical_cores: int

    computers: list[Computer] = Relationship(back_populates="cpus", link_model=ComputerCPULink)
    switches: list["Switch"] = Relationship(back_populates="cpu")


class Memory(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    capacity: int
    speed: int

    memory_slots: list["MemorySlot"] = Relationship(back_populates="memory")


class MemorySlot(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    slot_number: int

    computer_id: int | None = Field(default=None, foreign_key="computer.id", ondelete="CASCADE")
    switch_id: int | None = Field(default=None, foreign_key="switch.id")
    memory_id: int | None = Field(default=None, foreign_key="memory.id")

    computer: Computer | None = Relationship(back_populates="memory_slots")
    memory: Memory = Relationship(back_populates="memory_slots")
    switch: Switch | None = Relationship(back_populates="memory_slots")


class OS(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    version: str
    build: str

    computers: list[Computer] = Relationship(back_populates="oses", link_model=ComputerOSLink)


class PhysicalDisk(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    smart_status: str
    firmware: str

    computer_id: int | None = Field(default=None, foreign_key="computer.id", ondelete="CASCADE")
    physicaldisktype_id: int | None = Field(default=None, foreign_key="physicaldisktype.id")

    computer: Computer = Relationship(back_populates="physical_disks")
    physical_disk_type: "PhysicalDiskType" = Relationship(back_populates="physical_disks")
    volumes: "Volume" = Relationship(back_populates="physical_disk")


class PhysicalDiskType(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    model: str
    capacity: int
    type: str

    physical_disks: list[PhysicalDisk] = Relationship(back_populates="physical_disk_type")


class Volume(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    capacity: float
    file_system: str
    usage: str

    physicaldisk_id: int | None = Field(default=None, foreign_key="physicaldisk.id")

    physical_disk: PhysicalDisk = Relationship(back_populates="volumes")

class Firmware(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    switches: list[Switch] = Relationship(back_populates="firmware")

class Port(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    speed: int
    is_online: bool
    error_count: int
    description: str
    admin_status: bool
    is_uplink: bool

    port_type_id: int | None = Field(default=None, foreign_key="porttype.id")
    switch_id: int | None = Field(default=None, foreign_key="switch.id")
    vlan_id: int | None = Field(default=None, foreign_key="vlan.id")

    port_type: "PortType" = Relationship(back_populates="ports")
    switch: Switch = Relationship(back_populates="ports")
    vlan: "VLAN" = Relationship(back_populates="ports")
    local_ports: list[Neighbor] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Neighbor.local_port_id == Port.id"
        }
    )
    remote_ports: list[Neighbor] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Neighbor.remote_port_id == Port.id"
        }
    )
    port_fdb: "PortFDB" = Relationship(back_populates="port")


class PortType(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    ports: list[Port] = Relationship(back_populates="port_type")

class VLAN(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    name: str

    ports: list[Port] = Relationship(back_populates="vlan")

class PortFDB(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    vendor: str

    port_id: int | None = Field(default=None, foreign_key="port.id")
    mac_id: int | None = Field(default=None, foreign_key="mac.id")
    ip_id: int | None = Field(default=None, foreign_key="ip.id")

    port: Port = Relationship(back_populates="port_fdb")
    mac: MAC = Relationship(back_populates="port_fdb")
    ip: IP = Relationship(back_populates="port_fdb")