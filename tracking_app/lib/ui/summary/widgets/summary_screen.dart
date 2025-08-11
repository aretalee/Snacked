import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';

import 'package:Snacked/ui/summary/view_model/summary_vm.dart';
import 'package:Snacked/ui/archive/view_model/archive_vm.dart';

 
 class SummaryPage extends StatefulWidget {
  const SummaryPage({super.key, required this.viewModel, required this.viewModelA});
  final SummaryViewModel viewModel;
  final ArchiveViewModel viewModelA;

  @override
  State<SummaryPage> createState() => _SummaryPageState();
 }

class _SummaryPageState extends State<SummaryPage> {

  @override
  Widget build(BuildContext context) {
      return Scaffold (
        appBar: AppBar(
          title: Text('Summary for ${DateFormat('MMMM d, y').format(DateTime.now().subtract(Duration(days:1)))}', style: TextStyle(fontWeight: FontWeight.bold)), 
          backgroundColor: Colors.black, automaticallyImplyLeading:false),
        body: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              Text('See how you did today!', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Color.fromARGB(255, 205, 155, 249)), textAlign: TextAlign.center),
              const SizedBox(height:30),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Column(
                            children: [
                              Text('Eating:', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                              const SizedBox(height:15),
                              Text('${widget.viewModelA.eating} min', style: TextStyle(fontSize: 20, color: const Color.fromARGB(255, 39, 183, 255)), textAlign: TextAlign.center),
                            ]
                          ),
                          const SizedBox(width:50),
                          Column(
                            children: [
                              Text('Snacking:', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                              const SizedBox(height:15),
                              Text('${widget.viewModelA.snacking} min', style: TextStyle(fontSize: 20, color: Color.fromARGB(255, 39, 183, 255)), textAlign: TextAlign.center),
                            ]
                          )
                        ]
                      ),
                      const SizedBox(height:45),
                      Text('Compared to ${DateFormat('MMM d').format(DateTime.now().subtract(Duration(days:2)))}:', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                      const SizedBox(height:15),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          (widget.viewModelA.compIcon && !widget.viewModelA.noDiff) ? Text(widget.viewModelA.comparison, style: TextStyle(fontSize: 20, color: Color.fromARGB(255, 66, 255, 72))) 
                          : (widget.viewModelA.noDiff ? Text(widget.viewModelA.comparison, style: TextStyle(fontSize: 20, fontStyle: FontStyle.italic)) 
                          : Text(widget.viewModelA.comparison, style: TextStyle(fontSize: 20, color: Colors.yellow))),
                          const SizedBox(width:5),
                          (widget.viewModelA.compIcon && !widget.viewModelA.noDiff) ? Icon(Icons.arrow_downward, color: Color.fromARGB(255, 66, 255, 72), size: 20,) 
                          : (widget.viewModelA.noDiff ? Icon(Icons.swap_vert, color: Colors.white, size: 20,) 
                          : Icon(Icons.arrow_upward, color: Colors.yellow, size: 20,))
                        ]
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height:30),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Text('Based on your goals:', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                      const SizedBox(height:15),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          (widget.viewModelA.progressIcon) ? Text(widget.viewModelA.onTrack, style: TextStyle(fontSize: 20, color: Color.fromARGB(255, 66, 255, 72))) 
                          : Text(widget.viewModelA.onTrack, style: TextStyle(fontSize: 20, color: const Color.fromARGB(255, 255, 91, 244))),
                          const SizedBox(width:10),
                          (widget.viewModelA.progressIcon) ? Icon(Icons.thumb_up, color: Color.fromARGB(255, 66, 255, 72), size: 20,) 
                          : Icon(Icons.warning, color: const Color.fromARGB(255, 255, 91, 244), size: 20,)
                        ]
                      ),
                    ]
                  ),
                ),
              ),
              const SizedBox(height:30),
              FilledButton(
                onPressed: () => context.push('/home/comments'), 
                child: const Text('Add a comment'),
              ),
            ],
          )
        )
      );

  }

}





