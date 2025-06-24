import 'package:flutter/material.dart';

import 'package:snacktrac/data/repositories/auth_repository.dart';


class ChangePwdViewModel extends ChangeNotifier{
  final AuthRepository authRepo = AuthRepository();
  String _oldPwd = '';
  String _newPwd = '';

  void setOldPwd(String pwd) {
    _oldPwd = pwd;
  }

  void setNewPwd(String pwd) {
    _newPwd = pwd;
  }

  Future<String?> changePassword() async {
    try {
      final status = await authRepo.changePassword(_oldPwd, _newPwd);
      return status;
    } catch (e) {
      return e.toString();
    }
  }
  
}

