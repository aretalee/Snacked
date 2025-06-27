import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'package:snacktrac/ui/change_password/view_model/change_password_vm.dart';


class ChangePwdPage extends StatefulWidget {
  const ChangePwdPage({super.key, required this.viewModel});
  final ChangePwdViewModel viewModel;

  @override
  State<ChangePwdPage> createState() => _ChangePwdPageState();
}

class _ChangePwdPageState extends State<ChangePwdPage> {
  final TextEditingController _pwdControllerOne = TextEditingController();
  final TextEditingController _pwdControllerTwo = TextEditingController();
  final TextEditingController _pwdControllerOld = TextEditingController();

  @override
  void initState() {
    super.initState();
  }

  void dispose() {
    _pwdControllerOne.dispose();
    _pwdControllerTwo.dispose();
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
                  Text('Change Password', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold,)),
                  const SizedBox(height:30),
                    TextField(
                      obscureText: true,
                      controller: _pwdControllerOld,
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'Old password: ',
                        errorText: widget.viewModel.pwdErrorOld,
                      ),
                    ),
                    const SizedBox(height:15),
                    TextField(
                      obscureText: true,
                      controller: _pwdControllerOne,
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'New password: ',
                        errorText: widget.viewModel.pwdErrorOne,
                      ),
                    ),
                    const SizedBox(height:15),
                    TextField(
                      obscureText: true,
                      controller: _pwdControllerTwo,
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'Retype password: ',
                        errorText: widget.viewModel.pwdErrorTwo,
                      ),
                    ),
                    const SizedBox(height:30),
                    FilledButton(
                      onPressed: () async {
                        setState(() {
                          widget.viewModel.pwdErrors(_pwdControllerOld.text, _pwdControllerOne.text, _pwdControllerTwo.text);
                        });
                        if (widget.viewModel.pwdCheck(_pwdControllerOld.text, _pwdControllerOne.text, _pwdControllerTwo.text)) {
                          if (widget.viewModel.pwdSame(_pwdControllerOne.text, _pwdControllerTwo.text)) {
                            final changeStatus = await widget.viewModel.changePassword();
                            if (widget.viewModel.pwdSuccess(changeStatus)) {
                              ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                                content: Text('Successfully changed password', style: TextStyle(fontSize: 16, color:Colors.green, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                                duration: const Duration(seconds: 3),
                                )
                              );
                              context.go('/profile');
                            } else {
                              ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                                content: Text('$changeStatus', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                                duration: const Duration(seconds: 3),
                                )
                              );
                            }
                          } else {
                            ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                              content: Text('The typed passwords do not match', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                              duration: const Duration(seconds: 3),
                            )
                          );
                        };
                      };
                    }, 
                    child: const Text('Confirm'),
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




