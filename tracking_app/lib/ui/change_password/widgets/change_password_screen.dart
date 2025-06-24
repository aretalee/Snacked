import 'package:flutter/material.dart';

import 'package:snacktrac/ui/change_password/view_model/change_password_vm.dart';
import 'package:snacktrac/ui/profile/widgets/profile_screen.dart';
import 'package:snacktrac/ui/profile/view_model/profile_vm.dart';


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
  String? _pwdErrorOne;
  String? _pwdErrorTwo;
  String? _pwdErrorOld;

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
                      controller: _pwdControllerOld,
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'Old password: ',
                        errorText: _pwdErrorOld,
                      ),
                    ),
                    const SizedBox(height:15),
                    TextField(
                      controller: _pwdControllerOne,
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'New password: ',
                        errorText: _pwdErrorOne,
                      ),
                    ),
                    const SizedBox(height:15),
                    TextField(
                      controller: _pwdControllerTwo,
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'Retype password: ',
                        errorText: _pwdErrorTwo,
                      ),
                    ),
                    const SizedBox(height:30),
                    FilledButton(
                      onPressed: () async {
                        setState(() {
                        if (_pwdControllerOld.text.isEmpty) {
                          _pwdErrorOld = 'Please enter your old password';
                        } else { _pwdErrorOld = null; }
                        if (_pwdControllerOne.text.isEmpty) {
                          _pwdErrorOne = 'Please enter a password';
                        } else { _pwdErrorOne = null; }
                        if (_pwdControllerTwo.text.isEmpty) {
                          _pwdErrorTwo = 'Please enter a password';
                        } else { _pwdErrorTwo = null; }
                      });
                      if (_pwdErrorOne == null && _pwdErrorTwo == null) {
                        if (_pwdControllerOne.text == _pwdControllerTwo.text) {
                          widget.viewModel.setOldPwd(_pwdControllerOld.text);
                          widget.viewModel.setNewPwd(_pwdControllerOne.text);
                          final changeStatus = await widget.viewModel.changePassword();
                          if (changeStatus != null && changeStatus.contains('Success')) {
                            ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                                content: Text('Successfully changed password', style: TextStyle(fontSize: 16, color:Colors.green, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                                duration: const Duration(seconds: 3),
                                )
                              );
                              Navigator.push(
                                context, MaterialPageRoute(builder: (context) => ProfilePage(viewModel: ProfileViewModel())),
                              );
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




