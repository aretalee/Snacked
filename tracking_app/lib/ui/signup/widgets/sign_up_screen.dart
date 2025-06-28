import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'package:snacktrac/ui/signup/view_model/sign_up_vm.dart';


class SignUpPage extends StatefulWidget {
  const SignUpPage({super.key, required this.viewModel});
  final SignUpViewModel viewModel;

  @override
  State<SignUpPage> createState() => _SignUpPageState();
}


class _SignUpPageState extends State<SignUpPage> {
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
                  Text('Sign Up', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
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
                  const SizedBox(height:30),
                  FilledButton(
                    onPressed: () async {
                      setState(() {
                        widget.viewModel.registerErrors(_emailController.text, _pwdController.text);
                      });
                      if (widget.viewModel.registerCheck(_emailController.text, _pwdController.text)) {
                        final signUpStatus = await widget.viewModel.register();
                        if (widget.viewModel.registerSuccess(signUpStatus)) {
                          context.go('/summary');
                        } else{
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                            content: Text('$signUpStatus', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            duration: const Duration(seconds: 3),
                            )
                          );
                        }
                      }
                    },
                    child: const Text('Register'),
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

