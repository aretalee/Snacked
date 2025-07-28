import 'package:flutter/material.dart';
import 'dart:async';
import 'package:go_router/go_router.dart';

import 'package:Snacked/ui/summary/view_model/summary_vm.dart';
import 'package:Snacked/ui/archive/view_model/archive_vm.dart';
import 'package:Snacked/ui/summary/widgets/summary_screen.dart';
import 'package:Snacked/ui/summary/widgets/no_data_screen.dart';

 
 class HomePage extends StatefulWidget {
  const HomePage({super.key, required this.viewModel, required this.viewModelA});
  final SummaryViewModel viewModel;
  final ArchiveViewModel viewModelA;

  @override
  State<HomePage> createState() => _SummaryPageState();
 }

class _SummaryPageState extends State<HomePage> {
  final TextEditingController _commentsController = TextEditingController();
  Timer? _timer;
  late Future<bool> _newData;

  @override
  void initState() {
    super.initState();
    // if(!widget.viewModel.addedData) {
    //   widget.viewModel.setAddTrue;
    //   _newData = widget.viewModel.addData();
    // }
    widget.viewModelA.setDate(DateTime.now().subtract(Duration(days:1)));
    _newData = widget.viewModelA.getFromStorage();
    _timer = Timer(widget.viewModel.timerDuration(), () async {
      // widget.viewModel.setAddFalse;
      await widget.viewModel.addData();
      if (!widget.viewModel.promptShown()) {
        widget.viewModel.updateLastShown();
        widget.viewModel.showPrompt(context, widget.viewModel);
      }
    });
  }

  @override
  void dispose() {
    _commentsController.dispose();
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: _newData,
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if(snapshot.hasData) {
          // return Scaffold (
          //   body: Padding(
          //     padding: const EdgeInsets.all(20.0),
          //     child: Center(
          //       child: Column(
          //         mainAxisSize: MainAxisSize.min,
          //         children: [
          //           FilledButton(
          //             onPressed: () async {
          //               if (await widget.viewModelA.getFromStorage()) {
          //                 context.go('/home/summary');
          //               } else { context.go('/home/noData'); }
          //             }, 
          //             child: Padding(
          //             padding: const EdgeInsets.all(15.0),
          //               child: const Text('See daily summary'),
          //             ),
          //           ),
          //         ],
          //       )
          //     )
          //   )
          // );
          return SummaryPage(viewModel: widget.viewModel, viewModelA: widget.viewModelA);
        } else if (snapshot.hasError) { return NoDataSummary(); }
        else { return const Text('Loading'); }
        
      }
    );
  }

}





