import 'package:flutter/material.dart';

import 'package:Snacked/ui/set_goals/view_model/set_goals_vm.dart';


class SetGoalsPage extends StatefulWidget {
  const SetGoalsPage({super.key, required this.viewModel});
  final SetGoalsViewModel viewModel;

  @override
  State<SetGoalsPage> createState() => _SetGoalsPageState();
}

class _SetGoalsPageState extends State<SetGoalsPage> {
  final TextEditingController _goalController = TextEditingController();

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    _goalController.dispose();
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
                  Text('Set a Goal', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold,)),
                  const SizedBox(height:30),
                  TextField(
                    controller: _goalController,
                    decoration: InputDecoration(
                      border: OutlineInputBorder(),
                      hintText: 'Snacking time (in min): ',
                      errorText: widget.viewModel.goalError,
                    ),
                  ),
                  const SizedBox(height:15),
                  FilledButton(
                    onPressed: () async {
                      setState(() {
                        widget.viewModel.goalErrors(_goalController.text);
                      });
                      if (widget.viewModel.checkGoalInput(_goalController.text)) {
                        final updateStatus = await widget.viewModel.updateNewGoal();
                        if (updateStatus) {
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                              content: Text('Goal updated successfully.', style: TextStyle(fontSize: 16, color:Colors.green, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                              duration: const Duration(seconds: 1),
                            )
                          );
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                              content: Text('Unable to set goal, please try again.', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                              duration: const Duration(seconds: 1),
                            )
                          );
                        }
                      }
                    }, 
                    child: const Text('Save'),
                  ),
                  const SizedBox(height:5),
                  FilledButton(
                    onPressed: () async {
                      final checkGoal = await widget.viewModel.currentGoal;
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                        content: Text('Your current goal is $checkGoal min of snacking daily', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                        duration: const Duration(seconds: 2),
                      ));
                    }, 
                    child: const Text('Check current goal'),
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


