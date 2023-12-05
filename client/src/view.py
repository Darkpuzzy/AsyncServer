import random

test_disk_id = "CD123456789S"

random_id = [random.choice('abc123' if i != 5 else 'ABC') for i in range(20)]
disk_id = "".join(random_id)


class ManagerVM:
    """
    ram has unit GB !
    cpu has unit int Core max cores 5
    disk_size has unit GB !
    """

    def __init__(
            self,
            ram: int,
            cpu: int,
            disc: int
    ):
        self.id: int = None
        self.ram: int = ram
        self.cpu: int = cpu if cpu < 5 else 4
        self.disc: int = disc
        self.disc_id: str = disk_id

    async def get_base_info(self):
        return self.to_dict()

    async def get_full_info(self) -> dict:
        result = self.to_dict()
        result["ram"] = f"{self.ram} GB"
        result["disc"] = f"{self.disc} GB"
        return result

    def to_dict(self) -> dict:
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_') and value is not None}

    async def set_id(
            self,
            vm_id: int
    ) -> None:
        self.id: int = vm_id


# vm = ManagerVM(ram=10, cpu=20, disk_size=11)
#
# print(vm.__doc__)
# print(vm.get_full_info())
# print(vm.get_base_info())
