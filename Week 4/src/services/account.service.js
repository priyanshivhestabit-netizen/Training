const AccountRepository = require("../repositories/account.repository");

class AccountService {
  // Create new account
  static async create(data) {
    const existingAccount = await AccountRepository.findByEmail(data.email);

    if (existingAccount) {
      throw new Error("Account already exists with this email");
    }

    return await AccountRepository.create(data);
  }
}
module.exports = AccountService;