import 'package:flutter/material.dart';

import 'package:snacktrac/data/repositories/auth_repository.dart';
import 'package:snacktrac/ui/navigation_bar/widgets/navigation_bar.dart';
import 'package:snacktrac/ui/navigation_bar/view_model/navigation_bar_vm.dart';


class SignUpPage extends StatefulWidget {
  const SignUpPage({super.key});

  State<SignUpPage> createState() => _SignUpPageState();
}


class _SignUpPageState extends State<SignUpPage> {
  final AuthRepository authRepo = AuthRepository();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _pwdController = TextEditingController();
  String? _emailError;
  String? _pwdError;
  String? signUpError = '';

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
                  Text('Sign Up', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
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
                          _emailError = 'Please enter an email address';
                        } 
                        if (pwd.isEmpty) {
                          _pwdError = 'Please enter a password';
                        }
                      });
                      final signUpStatus = await authRepo.register (
                        _emailController.text, _pwdController.text
                      );
                      if (signUpStatus != null && signUpStatus.contains('Success')) {
                        Navigator.push(
                          context, MaterialPageRoute(builder: (context) => NavBar(viewModel: NavBarViewModel())),
                        );
                      } else{
                        setState(() {
                          signUpError = signUpStatus;
                        });
                      };
                    },
                    child: const Text('Register'),
                  ),
                  const SizedBox(height:15),
                  Text('$signUpError', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                ]
              )
            )
          )
        )
      )
    );
  }

}

