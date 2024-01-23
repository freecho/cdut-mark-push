// 引入axios
const axios = require('axios');

//引入JSEncrypt
window = {}
const JSEncrypt = require("jsencrypt")

//传入的password
var password = process.argv[2]; // 获取传入的参数

var encrypt = new JSEncrypt();

// var url = "https://cas.paas.cdut.edu.cn/cas/jwt/publicKey";
var publicKey = "-----BEGIN PUBLIC KEY----- MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyor3CX6A6U4EoSHawtALiJoB0CkJnb/wmVkcVT5EmNupGVrVSeJo80ZAxsgd9S1CZVXxTXtJ7XjsqnzR64Qvrn+tdvj9Ck5k/6Tnp6HoKU/AQxA3tQ5Zqw6D6ihPOyVV4z4cdK5wjzEBNPhJuTjjzP4VQ4h4VseWNbfhXGK3vSes8oNn5Wwor9r1UbEJP/ZMHrDJxAcwe0GPvebAqEp4O5ZcTtWnq+/qkoUB6z/52EnCMltoPmuMC+o3fWdICBf4q70oSDClfuhLVi4mRT2K5UUH8fsxEe6oPtkvk9vVCCOZRmo0MXpXZiIqdZOtgcBzn/0mzoNd58KxeIy0ginjfwIDAQAB -----END PUBLIC KEY-----";
encrypt.setPublicKey(publicKey);


encryptPassword = encrypt.encrypt(password)
console.log(encryptPassword)

