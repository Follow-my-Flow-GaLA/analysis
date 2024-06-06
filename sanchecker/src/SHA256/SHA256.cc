#include <iostream>
#include <sstream>
#include <iomanip>
#include <string>
#include <vector>

#include <openssl/sha.h>

class SHA256 {
public:
    static std::string hash(const std::string& originalData) {
        std::vector<unsigned char> utf8Data = convertToUTF8(originalData);
        SHA256_CTX sha256;
        SHA256_Init(&sha256);
        SHA256_Update(&sha256, utf8Data.data(), utf8Data.size());
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256_Final(hash, &sha256);
        return toHexString(hash, SHA256_DIGEST_LENGTH);
    }

private:
    static std::vector<unsigned char> convertToUTF8(const std::string& originalData) {
        std::vector<unsigned char> utf8Data(originalData.begin(), originalData.end());
        return utf8Data;
    }

    static std::string toHexString(const unsigned char* hash, size_t length) {
        std::stringstream ss;
        for (size_t i = 0; i < length; ++i) {
            ss << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(hash[i]);
        }
        return ss.str();
    }
};

int main() {
    std::string data = "\xa9 \x0a";
    std::string hashValue = SHA256::hash(data);
    std::cout << "Hash value: " << hashValue << std::endl;

    return 0;
}

