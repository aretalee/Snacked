import 'package:flutter/material.dart';

import 'package:Snacked/global.dart';


class LoginViewModel extends ChangeNotifier{
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

  Future<String?> login() async {
    try {
      final status = await authRepo.login(_email, _pwd);
      return status;
    } catch (e) {
      return e.toString();
    }
  }

  void loginErrors(String emailInput, String pwdInput) {
    if (emailInput.isEmpty) {
      _emailError = 'Please enter an email address';
    } 
    if (pwdInput.isEmpty) {
      _pwdError = 'Please enter a password';
    } 
  }

  bool loginCheck(String emailInput, String pwdInput) {
    if (_emailError == null && _pwdError == null) {
      setEmail(emailInput);
      setPwd(pwdInput);
      return true;
    }
    return false;
  }

  bool loginSuccess(String? status) {
    if (status != null && status.contains('Success')) {
      return true;
    }
    return false;
  }

  Future<String?> resetPassword() async {
    try {
      final status = await authRepo.resetPassword(_email);
      return status;
    } catch (e) {
      return e.toString();
    }
  }

  bool resetEmailCheck(String emailInput) {
    if (emailInput.isNotEmpty) {
      setEmail(emailInput);
      return true;
    }
    return false;
  }

  bool resetSuccess(String? status) {
    if (status != null && status.contains('Success')) {
      return true;
    }
    return false;
  }
  
}


