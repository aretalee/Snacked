import 'package:flutter/material.dart';

import 'package:snacktrac/data/repositories/auth_repository.dart';
import 'package:snacktrac/ui/navigation_bar/widgets/navigation_bar.dart';
import 'package:snacktrac/ui/navigation_bar/view_model/navigation_bar_vm.dart';


class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final AuthRepository authRepo = AuthRepository();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _pwdController = TextEditingController();
  String? _emailError;
  String? _pwdError;
  String? loginError = '';

  @override
  void initState() {
    super.initState();
  }

  void dispose() {
    _emailController.dispose();
    _pwdController.dispose();
    super.dispose();
  }

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
                      errorText: _emailError,
                    ),
                  ),
                  const SizedBox(height:15),
                  TextField(
                    controller: _pwdController,
                    decoration: InputDecoration(
                      border: OutlineInputBorder(),
                      hintText: 'Password: ',
                      errorText: _pwdError,
                    ),
                  ),
                  const SizedBox(height:30),
                  FilledButton(
                    onPressed: () async {
                      final email = _emailController.text;
                      final pwd = _pwdController.text;
                      setState(() {
                        _emailError = null;
                        _pwdError = null;
                        if (email.isEmpty) {
                          _emailError = 'Please enter your email address';
                        } 
                        if (pwd.isEmpty) {
                          _pwdError = 'Please enter your password';
                        }
                      });
                      final loginStatus = await authRepo.login (
                        _emailController.text, _pwdController.text
                      );
                      if (loginStatus != null && loginStatus.contains('Success')) {
                        Navigator.push(
                          context, MaterialPageRoute(builder: (context) => NavBar(viewModel: NavBarViewModel())),
                        );
                      } else {
                        setState(() {
                          loginError = loginStatus;
                        });
                        print(loginStatus);
                        print(loginError);
                      }
                    },
                    child: const Text('Go'),
                  ),
                  const SizedBox(height:15),
                  Text('$loginError', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                ]
              )
            )
          )
        )
      )
    );
  }
  
}