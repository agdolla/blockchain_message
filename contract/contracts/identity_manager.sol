pragma solidity ^0.4.7;

contract IdentityManager {
    string[100] users;
    uint latest;

    function new_identity(string uname) internal returns (uint) {

        if (latest >= 100) return 9999;

        users[latest] = uname;
        return latest++;
    }

    function get_identity(string uname) public returns (uint) {
         uint result = 999;

         for (uint i = 0; i < 100; i++) {
            if (stringsEqual(users[i], uname)) {
                result = i;
            }
         }

         if (result == 999) {
            result = new_identity(uname);
         }

         return result;
    }

    function stringsEqual(string storage _a, string memory _b) internal view returns (bool) {
		bytes storage a = bytes(_a);
		bytes memory b = bytes(_b);
		if (a.length != b.length)
			return false;
		for (uint i = 0; i < a.length; i ++)
			if (a[i] != b[i])
				return false;
		return true;
	}
}