import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

// import 'package:Snacked/ui/summary/view_model/summary_vm.dart';


 class PromptPage extends StatefulWidget {
  const PromptPage({super.key});

  @override
  State<PromptPage> createState() => _PromptPageState();
 }

class _PromptPageState extends State<PromptPage> {

  @override
  Widget build(BuildContext context) {
    return Dialog.fullscreen(
      child: Padding(
        padding: const EdgeInsets.all(35.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text('Do you think you snacked more or less than yesterday?', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
            const SizedBox(height:10),
            Text('Choose an option below to see!', style: TextStyle(fontSize: 16), textAlign: TextAlign.center),
            const SizedBox(height:30),
            FilledButton(
              onPressed: () {
                context.pop();
              },
              child: const Text('Less than before'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {
                context.pop();
              },
              child: const Text('More than before'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {
                context.pop();
              },
              child: const Text('Not very sure'),
            ),
            const SizedBox(height:30),
          ]
        )
      )
    );
  }
}


