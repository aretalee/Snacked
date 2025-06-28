import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'package:snacktrac/ui/login/view_model/login_vm.dart';


class LoginPage extends StatefulWidget {
  const LoginPage({super.key, required this.viewModel});
  final LoginViewModel viewModel;

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _pwdController = TextEditingController();

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    _emailController.dispose();
    _pwdController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold (
      appBar: AppBar(backgroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(30.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text('Login', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold,)),
                  const SizedBox(height:15),
                  TextField(
                    controller: _emailController,
                    decoration: InputDecoration(
                      border: OutlineInputBorder(),
                      hintText: 'Email: ',
                      errorText: widget.viewModel.emailError,
                    ),
                  ),
                  const SizedBox(height:15),
                  TextField(
                    obscureText: true,
                    controller: _pwdController,
                    decoration: InputDecoration(
                      border: OutlineInputBorder(),
                      hintText: 'Password: ',
                      errorText: widget.viewModel.pwdError,
                    ),
                  ),
                  const SizedBox(height:15),
                   OutlinedButton(
                    onPressed: () async {
                      if (widget.viewModel.resetEmailCheck(_emailController.text)) {
                        final resetStatus = await widget.viewModel.resetPassword();
                        if (widget.viewModel.resetSuccess(resetStatus)) {
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                              content: Text('If an account is linked to this email, you will receive a reset link shortly.', style: TextStyle(fontSize: 16, color:Colors.green, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                              duration: const Duration(seconds: 5),
                            )
                          );
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                              content: Text('$resetStatus', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                              duration: const Duration(seconds: 3),
                            )
                          );
                        }
                      };
                    },
                    child: const Text('Forgot password'),
                  ),
                  const SizedBox(height:5),
                  FilledButton(
                    onPressed: () async {
                      setState(() {
                        widget.viewModel.loginErrors(_emailController.text, _pwdController.text);
                      });
                      if (widget.viewModel.loginCheck(_emailController.text, _pwdController.text)) {
                        final loginStatus = await widget.viewModel.login();
                        if (widget.viewModel.loginSuccess(loginStatus)) {
                          context.go('/summary'); // is this still needed if there's also logic
                        } else{
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                            content: Text('$loginStatus', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            duration: const Duration(seconds: 3),
                            )
                          );
                        }
                      }
                    },
                    child: const Text('Go'),
                  ),
                ]
              )
            )
          )
        )
      )
    );
  }
  
}