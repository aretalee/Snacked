import 'package:flutter/material.dart';

import 'package:snacktrac/ui/signup/widgets/sign_up_screen.dart';
import 'package:snacktrac/ui/login/widgets/login_screen.dart';
import 'package:snacktrac/ui/signup/view_model/sign_up_vm.dart';
import 'package:snacktrac/ui/login/view_model/login_vm.dart';


class SignInPage extends StatelessWidget {
  const SignInPage({super.key});

  @override
  Widget build(BuildContext context) {

    return Scaffold (
      appBar: AppBar(backgroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => SignUpPage(viewModel: SignUpViewModel())),
                );
              }, 
              child: const Text('Sign Up'), 
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => LoginPage(viewModel: LoginViewModel())),
                );
              }, 
              child: const Text('Login'),
            ),
          ],
        )
      )
    );
  }

}


