import 'package:flutter/material.dart';

import 'package:Snacked/global.dart';


class ChangePwdViewModel extends ChangeNotifier{
  String _oldPwd = '';
  String _newPwd = '';
  String? _pwdErrorOne;
  String? _pwdErrorTwo;
  String? _pwdErrorOld;

  void setOldPwd(String pwd) {
    _oldPwd = pwd;
  }

  void setNewPwd(String pwd) {
    _newPwd = pwd;
  }

  String? get pwdErrorOld => _pwdErrorOld;
  String? get pwdErrorOne => _pwdErrorOne;
  String? get pwdErrorTwo => _pwdErrorTwo;

  Future<String?> changePassword() async {
    try {
      final status = await authRepo.changePassword(_oldPwd, _newPwd);
      return status;
    } catch (e) {
      return e.toString();
    }
  }

  void pwdErrors(String pwdInputOld, String pwdInputOne, String pwdInputTwo) {
    if (pwdInputOld.isEmpty) {
      _pwdErrorOld = 'Please enter your old password';
    } 
    if (pwdInputOne.isEmpty) {
      _pwdErrorOne = 'Please enter a password';
    } 
    if (pwdInputTwo.isEmpty) {
      _pwdErrorTwo = 'Please enter a password';
    }
  }

  bool pwdCheck(String pwdInputOld, String pwdInputOne, String pwdInputTwo) {
    if (_pwdErrorOld == null && _pwdErrorOne == null && _pwdErrorTwo == null) {
      setOldPwd(pwdInputOld);
      setNewPwd(pwdInputOne);
      return true;
    }
    return false;
  }

  bool pwdSame(String pwdInputOne, String pwdInputTwo) {
    if ( pwdInputOne == pwdInputTwo ) { return true; }
    return false;
  }

  bool pwdSuccess(String? status) {
    if (status != null && status.contains('Success')) {
      return true;
    }
    return false;
  }
  
}

