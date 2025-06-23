import 'package:firebase_auth/firebase_auth.dart';



class AuthRepository {
  final _auth = FirebaseAuth.instance;

  User? get currentUser => _auth.currentUser!;
  Stream<User?> get userChanges => _auth.userChanges();

  Future<UserCredential?> register(String email, String password) async {
    try {
      UserCredential credential = await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
      return credential;
    } on FirebaseAuthException catch (e) {
      if (e.code == 'email-already-in-use') {
        print('An account is already associated with this email.');
      } else if (e.code == 'email-already-in-use') {
        print('Chosen password is too weak.');
      } 
    } catch (e) {
        print(e);
      }
    return null;
  }

  Future<UserCredential?> login(String email, String password) async {
    try {
      UserCredential credential = await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
      return credential;
    } on FirebaseAuthException catch (e) {
      if (e.code == 'wrong-password') {
        print('Incorrect password.');
      } else if (e.code == 'user-not-found') {
        print('No account created under this email.');
      } 
    } catch (e) {
        print(e);
      }
    return null;
  }

  Future<void> signOut () async {
    await _auth.signOut();
  }

}

