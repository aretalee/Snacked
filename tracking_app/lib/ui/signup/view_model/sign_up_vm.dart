import 'package:flutter/material.dart';

import 'package:snacktrac/global.dart';



class SignUpViewModel extends ChangeNotifier{
  String _email = '';
  String _pwd = '';
  String? _emailError;
  String? _pwdError;

  void setEmail(String email) {
    _email = email;
  }

  void setPwd(String pwd) {
    _pwd = pwd;
  }

  String? get emailError => _emailError;
  String? get pwdError => _pwdError;

  Future<String?> register() async {
    try {
      final status = await authRepo.register(_email, _pwd);
      return status;
    } catch (e) {
      return e.toString();
    }
  }

  void registerErrors(String emailInput, String pwdInput) {
    if (emailInput.isEmpty) {
      _emailError = 'Please enter an email address';
    } 
    if (pwdInput.isEmpty) {
      _pwdError = 'Please enter a password';
    } 
  }

  bool registerCheck(String emailInput, String pwdInput) {
    if (_emailError == null && _pwdError == null) {
      setEmail(emailInput);
      setPwd(pwdInput);
      return true;
    }
    return false;
  }

  bool registerSuccess(String? status) {
    if (status != null && status.contains('Success')) {
      return true;
    }
    return false;
  }
  
}


